# GTA San Andreas ZON Import/Export for Blender 4.0

A lightweight add-on to load and save GTA San Andreas `.zon` files as 3D wireframe boxes.

## What It Is

- **Import** tool for `.zon` files: creates one wireframe box per zone, named and tagged with its type, flags and parent.
- **Export** tool: scans those boxes and writes a valid `.zon` file (with a `zone` header and an `end` footer) preserving all metadata.

## How It Works

1. **Import .zon File**  
   - Reads each line (skipping `zone`/`end`)  
   - Parses zone name, type, two corner coordinates, flag and parent  
   - Builds a Blender wireframe box at the correct world coordinates  
   - Stores metadata in custom object properties  

2. **Edit in Blender**  
   - Move, scale or rotate the boxes to adjust zone bounds  
   - Metadata follows each object automatically  

3. **Export .zon File**  
   - Finds all objects created by the importer  
   - Computes their world-space bounding corners  
   - Writes out lines in the original format, surrounded by `zone`/`end`

##Preview

![Screenshot 2025-05-06 173727](https://github.com/user-attachments/assets/ddbdaf6d-f37d-48c5-842b-47151f922e6b)
![Screenshot 2025-05-06 173748](https://github.com/user-attachments/assets/41df48d2-b8a0-42c6-b0e6-4092fc7abd9a)

## Example `.zon` Content

```zon
zone
LDT8, 0, 1507.51, -1385.21, 110.916, 1582.55, -1325.31, 335.916, 1, LDT
GANTON, 0, 2222.50, -1722.50, 15.000, 2722.50, -1222.50, 115.000, 0, LA
end
