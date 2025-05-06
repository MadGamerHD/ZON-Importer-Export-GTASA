bl_info = {
    "name": "ZON Zone Importer/Exporter",
    "author": "MadGamerHD",
    "version": (1, 2),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Zone Importer",
    "description": "Import and export GTA SA .zon files as box hitboxes",
    "category": "Import-Export",
}

import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper


def parse_zon(filepath):
    zones = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.lower() == 'end' or line.lower() == 'zone':
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 10:
                continue
            name = parts[0]
            zone_type = parts[1]
            x1, y1, z1 = map(float, parts[2:5])
            x2, y2, z2 = map(float, parts[5:8])
            flag = parts[8]
            parent = parts[9]
            zones.append((name, zone_type, (x1, y1, z1), (x2, y2, z2), flag, parent))
    return zones


def create_box(name, zone_type, c1, c2, flag, parent):
    cx = (c1[0] + c2[0]) / 2.0
    cy = (c1[1] + c2[1]) / 2.0
    cz = (c1[2] + c2[2]) / 2.0
    dx = abs(c2[0] - c1[0])
    dy = abs(c2[1] - c1[1])
    dz = abs(c2[2] - c1[2])

    mesh = bpy.data.meshes.new(f"{name}_mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    verts = [
        (cx - dx/2, cy - dy/2, cz - dz/2),
        (cx + dx/2, cy - dy/2, cz - dz/2),
        (cx + dx/2, cy + dy/2, cz - dz/2),
        (cx - dx/2, cy + dy/2, cz - dz/2),
        (cx - dx/2, cy - dy/2, cz + dz/2),
        (cx + dx/2, cy - dy/2, cz + dz/2),
        (cx + dx/2, cy + dy/2, cz + dz/2),
        (cx - dx/2, cy + dy/2, cz + dz/2),
    ]
    faces = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(1,2,6,5),(0,3,7,4)]
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj.display_type = 'WIRE'
    obj.show_in_front = True

    # store zone metadata
    obj["zone_type"] = zone_type
    obj["zone_flag"] = flag
    obj["zone_parent"] = parent
    return obj


class IMPORT_OT_zon(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.zon"
    bl_label = "Import ZON Zones"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext = ".zon"
    filter_glob: StringProperty(default="*.zon", options={'HIDDEN'})

    def execute(self, context):
        zones = parse_zon(self.filepath)
        for name, ztype, c1, c2, flag, parent in zones:
            create_box(name, ztype, c1, c2, flag, parent)
        self.report({'INFO'}, f"Imported {len(zones)} zones")
        return {'FINISHED'}


class EXPORT_OT_zon(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.zon"
    bl_label = "Export ZON Zones"
    bl_options = {'PRESET'}

    filename_ext = ".zon"
    filter_glob: StringProperty(default="*.zon", options={'HIDDEN'})

    def execute(self, context):
        objects = [obj for obj in context.scene.objects if "zone_type" in obj]
        with open(self.filepath, 'w') as f:
            # write header
            f.write("zone\n")
            for obj in objects:
                coords = [obj.matrix_world @ v.co for v in obj.data.vertices]
                xs = [v.x for v in coords]; ys = [v.y for v in coords]; zs = [v.z for v in coords]
                x1, x2 = min(xs), max(xs)
                y1, y2 = min(ys), max(ys)
                z1, z2 = min(zs), max(zs)
                line = f"{obj.name}, {obj['zone_type']}, {x1:.3f}, {y1:.3f}, {z1:.3f}, {x2:.3f}, {y2:.3f}, {z2:.3f}, {obj['zone_flag']}, {obj['zone_parent']}\n"
                f.write(line)
            # write footer
            f.write("end\n")
        self.report({'INFO'}, f"Exported {len(objects)} zones to {self.filepath}")
        return {'FINISHED'}


class ZON_PT_panel(bpy.types.Panel):
    bl_label = "ZON Zone Importer/Exporter"
    bl_idname = "ZON_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Zone Importer'

    def draw(self, context):
        layout = self.layout
        layout.operator(IMPORT_OT_zon.bl_idname, text="Import .zon File")
        layout.operator(EXPORT_OT_zon.bl_idname, text="Export .zon File")


def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_zon.bl_idname, text="ZON Zone (.zon)")


def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_zon.bl_idname, text="ZON Zone (.zon)")


def register():
    bpy.utils.register_class(IMPORT_OT_zon)
    bpy.utils.register_class(EXPORT_OT_zon)
    bpy.utils.register_class(ZON_PT_panel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ZON_PT_panel)
    bpy.utils.unregister_class(EXPORT_OT_zon)
    bpy.utils.unregister_class(IMPORT_OT_zon)


if __name__ == '__main__':
    register()
