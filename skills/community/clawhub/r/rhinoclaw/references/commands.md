# RhinoClaw Command Reference

## Connection Commands

### ping
Test connection to Rhino plugin.
```bash
python scripts/rhino_client.py ping
```

## Document Commands

### get_document_info
Get information about the current Rhino document (objects, layers, materials).
```bash
python scripts/rhino_client.py info
# or
python scripts/rhino_client.py get_document_info
```

Returns: objects (max 30), layers, materials, views, current layer.

### get_object_info
Get detailed info about a specific object.
```bash
python scripts/rhino_client.py get_object_info -p '{"id": "guid-here"}'
```

### get_selected_objects_info
Get info about currently selected objects.
```bash
python scripts/rhino_client.py get_selected_objects_info
```

## Geometry Commands

### Supported Geometry Types
- `POINT` - Single point
- `LINE` - Line from start to end
- `POLYLINE` - Connected line segments
- `CIRCLE` - Circle with radius
- `ARC` - Arc segment
- `ELLIPSE` - Ellipse
- `CURVE` - NURBS curve
- `BOX` - Rectangular box
- `SPHERE` - Sphere with radius
- `CONE` - Cone with radius and height
- `CYLINDER` - Cylinder with radius and height
- `SURFACE` - Surface from points
- `MESH` - Mesh geometry

### create_object
Create a single geometry object.

**Sphere:**
```bash
python scripts/geometry.py sphere --radius 5 --position 0,0,0 --name "MySphere"
```

**Box:**
```bash
python scripts/geometry.py box --width 10 --length 20 --height 5 --color 255,0,0
```

**Cylinder:**
```bash
python scripts/geometry.py cylinder --radius 2 --height 10 --layer "MyLayer"
```

**Line:**
```bash
python scripts/geometry.py line --start 0,0,0 --end 10,10,10
```

**Raw JSON:**
```bash
python scripts/geometry.py raw --type SPHERE --params '{"radius": 5}'
```

### create_objects (batch)
Create multiple objects at once - more efficient for many objects.
```bash
python scripts/rhino_client.py create_objects -p '{
  "objects": [
    {"type": "SPHERE", "params": {"radius": 1}, "translation": [0,0,0]},
    {"type": "SPHERE", "params": {"radius": 1}, "translation": [5,0,0]},
    {"type": "SPHERE", "params": {"radius": 1}, "translation": [10,0,0]}
  ]
}'
```

### delete_object
Delete an object by ID.
```bash
python scripts/rhino_client.py delete_object -p '{"id": "guid-here"}'
```

### modify_object
Modify an existing object's properties.
```bash
python scripts/rhino_client.py modify_object -p '{
  "id": "guid-here",
  "color": [255, 0, 0],
  "name": "NewName"
}'
```

### select_objects
Select objects by filter criteria.
```bash
python scripts/rhino_client.py select_objects -p '{
  "filters": {"name": "Sphere*", "layer": "Default"},
  "logic": "and"
}'
```

## Layer Commands

### create_layer
```bash
python scripts/layers.py create "MyLayer" --color 255,100,100
```

### delete_layer
```bash
python scripts/layers.py delete "MyLayer"
```

### set current layer
```bash
python scripts/layers.py set "MyLayer"
```

### get current layer
```bash
python scripts/layers.py current
```

### list layers
```bash
python scripts/layers.py list
```

## Material Commands

### create_material (legacy)
```bash
python scripts/materials.py create "Gold" --color 255,215,0 --shine 0.9
```

### create PBR material
```bash
python scripts/materials.py pbr "Gold_PBR" --color 255,215,0 --metallic 0.95 --roughness 0.05
```

### preset materials
```bash
python scripts/materials.py preset gold    # Gold PBR
python scripts/materials.py preset silver  # Silver PBR
python scripts/materials.py preset copper  # Copper PBR
```

### assign material to layer
```bash
python scripts/materials.py assign "MyLayer" "0"  # material_id from create
```

## Script Execution

### execute_rhinoscript_python_code
Execute arbitrary RhinoScript Python code.

**Inline:**
```bash
python scripts/script_exec.py -c "import rhinoscriptsyntax as rs; rs.AddSphere([0,0,0], 5)"
```

**From file:**
```bash
python scripts/script_exec.py -f myscript.py
```

**From stdin:**
```bash
echo "import rhinoscriptsyntax as rs; rs.AddLine([0,0,0], [10,10,10])" | python scripts/script_exec.py -s
```

## Debug Commands

### set_debug_mode
Enable/disable verbose logging.
```bash
python scripts/rhino_client.py set_debug_mode -p '{"enable": true}'
```

### log_thought
Log AI thought process (for traceability).
```bash
python scripts/rhino_client.py log_thought -p '{"thought": "Creating geometry..."}'
```

## Parameter Conventions

### Colors
RGB values 0-255: `[255, 128, 0]` or CLI: `255,128,0`

### Points/Coordinates
XYZ values: `[x, y, z]` or CLI: `0,0,0`

### IDs
GUID strings from Rhino: `"12345678-1234-1234-1234-123456789abc"`

## Common Workflows

### Create PBR scene with materials
```bash
# 1. Create layer
python scripts/layers.py create "Gold_Layer" --color 255,215,0

# 2. Create PBR material
python scripts/materials.py pbr "Gold_PBR" --color 255,215,0 --metallic 0.95 --roughness 0.05
# Note the material_id from output (e.g., "0")

# 3. Assign material to layer
python scripts/materials.py assign "Gold_Layer" "0"

# 4. Set current layer
python scripts/layers.py set "Gold_Layer"

# 5. Create object (inherits material from layer)
python scripts/geometry.py sphere --radius 2 --name "Gold_Sphere"
```

### Batch create objects
```bash
python scripts/rhino_client.py create_objects -p '{
  "objects": [
    {"type": "BOX", "params": {"width":1,"length":1,"height":1}, "translation": [0,0,0], "name": "Box1"},
    {"type": "BOX", "params": {"width":1,"length":1,"height":1}, "translation": [2,0,0], "name": "Box2"},
    {"type": "BOX", "params": {"width":1,"length":1,"height":1}, "translation": [4,0,0], "name": "Box3"}
  ]
}'
```
