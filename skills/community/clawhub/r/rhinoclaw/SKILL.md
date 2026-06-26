---
name: rhinoclaw
version: 0.2.5
description: >
  Control Rhino 3D via AI agents. 72+ tools for geometry, transforms, booleans,
  PBR materials, Grasshopper automation, VisualARQ BIM objects, and viewport control.
  Create parametric models, architectural layouts, and export to IFC — all from your terminal.
  Optional VisualARQ integration for walls, doors, windows, levels, and IFC workflows.
  Requires RhinoClaw plugin running in Rhino 7/8 on Windows.
author: McMuff86
repository: https://github.com/McMuff86/RhinoClaw
tags:
  - rhino
  - 3d
  - cad
  - bim
  - grasshopper
  - visualarq
  - parametric
  - architecture
  - manufacturing
  - ifc
---

# RhinoClaw Skill

Control Rhino 3D directly via TCP socket connection to the RhinoClaw plugin. 72+ tools for geometry creation, BIM workflows, Grasshopper automation, and more.

**Plugin:** [github.com/McMuff86/RhinoClaw](https://github.com/McMuff86/RhinoClaw) · **Author:** [Solid AI](https://solid-ai.ai)

## Prerequisites

1. **Rhino 7/8** running on Windows
2. **RhinoClaw plugin** installed and built
3. **Plugin started**: In Rhino command line, type `tcpstart` (for WSL/remote access)

> **Note:** Use `mcpstart` for local-only access (Cursor, Claude Desktop), `tcpstart` for WSL/Clawdbot.

## Configuration

Copy `config.example.json` to `config.json` and edit:

```bash
cp config.example.json config.json
```

```json
{
  "connection": {
    "host": "YOUR_RHINO_HOST_IP",
    "port": 1999,
    "timeout": 15.0
  },
  "screenshots": {
    "linux_dir": "./captures",
    "windows_dir": ""
  }
}
```

**Host IP depends on your setup:**
- **Same machine:** `127.0.0.1`
- **WSL2 → Windows:** Your gateway IP (`ip route show default | awk '{print $3}'`)
- **Remote (Tailscale/LAN):** The IP of the Windows machine running Rhino

## Quick Test

```bash
cd ~/clawd/skills/rhinoclaw/scripts
python3 rhino_client.py ping
```

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `rhino_client.py` | Base TCP client, raw commands |
| `geometry.py` | Create primitives (box, sphere, cylinder, curves...) |
| `transforms.py` | Move, rotate, scale, copy, mirror, arrays |
| `booleans.py` | Union, difference, intersection |
| `selection.py` | Select by layer, type, name, IDs |
| `analysis.py` | Object info, properties, bounding box, volume |
| `curves.py` | Offset, fillet, chamfer, join, explode |
| `surfaces.py` | Loft, extrude, revolve, sweep |
| `layers.py` | Create, set, list, delete layers |
| `materials.py` | PBR materials, assign to layers |
| `viewport.py` | Views, camera, screenshots |
| `render.py` | Lights, render settings, render to file |
| `files.py` | Open, save, import, export (STEP, OBJ, STL...) |
| `groups.py` | Groups and block definitions |
| `scene.py` | Document info, batch operations |
| `presets.py` | Preset & Template manager for GH definitions |
| `ghscript.py` | GH Definition builder + Compute Platform deployer |
| `visualarq.py` | VisualARQ BIM objects (walls, doors, windows, levels, IFC) |
| `utils.py` | Shared utilities (parse_coords, parse_color, format_result) |

---

## 🎯 Geometry Creation

```bash
# Primitives
python3 geometry.py sphere --radius 5 --position 0,0,0 --name "Ball"
python3 geometry.py box --width 10 --length 10 --height 5 --color 255,0,0
python3 geometry.py cylinder --radius 2 --height 8 --layer "Parts"
python3 geometry.py cone --radius 3 --height 6
python3 geometry.py line --start 0,0,0 --end 10,10,0
python3 geometry.py circle --radius 5
python3 geometry.py arc --radius 5 --angle 90
python3 geometry.py polyline --points "0,0,0 10,0,0 10,10,0 0,10,0"
```

### Supported Geometry Types

| Type | Key Parameters |
|------|----------------|
| POINT | location |
| LINE | start, end |
| POLYLINE | points |
| CIRCLE | center, radius |
| ARC | center, radius, angle |
| ELLIPSE | center, radius_x, radius_y |
| CURVE | points, degree |
| BOX | width, length, height |
| SPHERE | radius |
| CONE | radius, height |
| CYLINDER | radius, height |
| MESH | vertices, faces |

---

## 🔨 Solid Operations

```bash
# Fillet (round) edges of a solid
python3 solids.py fillet <object_id> --radius 2.0

# Fillet specific edges only
python3 solids.py fillet <object_id> --radius 2.0 --edges 0,1,3

# Chamfer edges
python3 solids.py chamfer <object_id> --distance 1.5

# Keep original (don't delete input)
python3 solids.py fillet <object_id> --radius 2.0 --keep
```

---

## 🔄 Transform Operations

```bash
# Move object
python3 transforms.py move <id> --vector 10,0,0

# Rotate object (degrees around axis through point)
python3 transforms.py rotate <id> --angle 45 --axis 0,0,1 --center 0,0,0

# Scale object
python3 transforms.py scale <id> --factor 2.0 --center 0,0,0

# Copy with offset
python3 transforms.py copy <id> --offset 10,0,0

# Mirror across plane
python3 transforms.py mirror <id> --origin 0,0,0 --normal 1,0,0

# Linear array: 5 copies along X
python3 transforms.py linear <id> --direction 1,0,0 --count 5 --distance 10

# Polar array: 8 copies around Z axis
python3 transforms.py polar <id> --center 0,0,0 --axis 0,0,1 --count 8
```

---

## ⚡ Boolean Operations

```bash
# Union multiple solids
python3 booleans.py union <id1> <id2> <id3>

# Difference: subtract cutter(s) from base
python3 booleans.py difference <base_id> <cutter_id>

# Intersection
python3 booleans.py intersection <id1> <id2>

# Keep input objects (don't delete)
python3 booleans.py union <id1> <id2> --keep
```

> **Note:** Objects must be closed solids (Breps).

---

## 🎯 Selection

```bash
# Select all
python3 selection.py all

# Clear selection
python3 selection.py none

# Get info about selected objects
python3 selection.py get

# Select by layer
python3 selection.py layer "MyLayer"

# Select by object type
python3 selection.py type solid    # solid, curve, surface, mesh, point, etc.

# Select by name (partial match)
python3 selection.py name "Box"

# Select specific IDs
python3 selection.py ids <id1> <id2> <id3>

# Combined filters
python3 selection.py filter --layer "Parts" --type solid
```

---

## 📊 Object Analysis

```bash
# Basic object info
python3 analysis.py info <object_id>

# Detailed properties (bounding box, area, volume, centroid)
python3 analysis.py properties <object_id>

# Info about selected objects
python3 analysis.py selected

# Document summary
python3 analysis.py document
```

---

## 〰️ Curve Operations

```bash
# Offset curve
python3 curves.py offset <curve_id> --distance 5

# Fillet two curves
python3 curves.py fillet <curve1_id> <curve2_id> --radius 2

# Chamfer two curves
python3 curves.py chamfer <curve1_id> <curve2_id> --distance 3

# Join curves into polycurve
python3 curves.py join <id1> <id2> <id3>

# Explode polycurve into segments
python3 curves.py explode <polycurve_id>

# Keep input (don't delete)
python3 curves.py join <id1> <id2> --keep
```

---

## 🏔️ Surface Operations

```bash
# Loft through curves
python3 surfaces.py loft <curve1_id> <curve2_id> <curve3_id>

# Extrude curve along vector
python3 surfaces.py extrude <curve_id> --direction 0,0,10

# Revolve curve around axis
python3 surfaces.py revolve <curve_id> --axis-start 0,0,0 --axis-end 0,0,1 --angle 360

# Sweep curve along rail
python3 surfaces.py sweep <profile_id> <rail_id>

# Create planar surface from closed curve
python3 surfaces.py planar <closed_curve_id>
```

---

## 📁 Layers

```bash
python3 layers.py create "MyLayer" --color 255,100,100
python3 layers.py set "MyLayer"
python3 layers.py list
python3 layers.py delete "OldLayer"
```

---

## 🎨 Materials (PBR)

```bash
# Metal presets
python3 materials.py preset gold
python3 materials.py preset silver
python3 materials.py preset copper

# Custom PBR material
python3 materials.py pbr "Chrome" --color 200,200,210 --metallic 0.95 --roughness 0.02

# Assign material to layer
python3 materials.py assign "MyLayer" <material_id>
```

---

## 📷 Viewport & Screenshots

```bash
# Set standard view
python3 viewport.py view Perspective
python3 viewport.py view Top

# Zoom to fit all
python3 viewport.py zoom

# Zoom to selection
python3 viewport.py zoom --selected

# Orbit camera
python3 viewport.py orbit --yaw 45 --pitch 30

# Set camera position
python3 viewport.py camera --position 100,100,50 --target 0,0,0 --lens 35

# Capture screenshot (saves to linux_dir, returns linux_path)
python3 viewport.py screenshot --width 1920 --height 1080
python3 viewport.py screenshot --output myrender.png

# Render with materials
python3 viewport.py render --output render.png
```

> **Screenshots** are saved directly to the Linux filesystem via WSL UNC path. The returned `linux_path` can be read directly.

---

## 💡 Render & Lighting

```bash
# Set render quality
python3 render.py settings --width 1920 --height 1080 --quality high
python3 render.py settings --background 50,50,50

# Add lights
python3 render.py light point --position 50,50,100 --intensity 1.5
python3 render.py light directional --direction -1,-1,-1
python3 render.py light spot --position 0,0,100 --target 0,0,0

# Render to file
python3 render.py render --output scene.png
```

---

## 📦 Files (Import/Export)

```bash
# Open 3DM file
python3 files.py open "/path/to/file.3dm"

# Save current document
python3 files.py save
python3 files.py save --path "/path/to/new.3dm"

# Export to various formats
python3 files.py export output.step
python3 files.py export output.obj --ids <id1> <id2>
python3 files.py export output.stl --format stl

# Import mesh
python3 files.py import model.obj
```

### Supported Export Formats
STEP, IGES, OBJ, STL, DXF, DWG, 3DS, FBX, DAE

---

## 📦 Groups & Blocks

```bash
# Create group
python3 groups.py group <id1> <id2> --name "MyGroup"

# Ungroup
python3 groups.py ungroup --name "MyGroup"

# Create block definition
python3 groups.py block-create "MyBlock" <id1> <id2> --base 0,0,0

# Insert block instance
python3 groups.py block-insert "MyBlock" --position 10,0,0 --scale 2 --rotation 45

# Explode block
python3 groups.py block-explode <instance_id>
```

---

## 🌿 Grasshopper Player Automation

Run Grasshopper definitions with custom parameters directly from CLI.

```bash
# Show available parameters in a GH file
python3 grasshopper.py info "C:/path/to/definition.gh"

# Run with default parameters
python3 grasshopper.py run "C:/path/to/definition.gh"

# Run with custom parameters
python3 grasshopper.py run "C:/path/to/definition.gh" --Lichthoehe 2200 --Lichtbreite 1000

# Set insertion point
python3 grasshopper.py run "C:/path/to/definition.gh" --Point 100,200,0
```

### Parameter Discovery

```bash
python3 grasshopper.py info "C:/path/to/definition.gh"
# Output shows: parameter name, default value, min/max range, type
```

### How It Works

1. `info` loads the GH file via Grasshopper SDK to extract parameter metadata
2. `run` starts Rhino's GrasshopperPlayer via `SendKeystrokes` (non-blocking)
3. Script monitors command prompts and sends parameter values
4. `Get Point` prompts receive the `--Point` coordinate or default `0,0,0`

### Presets (YAML-based)

```bash
# List available presets
python3 grasshopper.py preset --list

# Run a preset
python3 grasshopper.py preset door_standard

# Override preset parameters
python3 grasshopper.py preset door_standard --Lichthoehe 2200
```

Presets are defined in `config/presets.yaml`, templates in `config/templates.yaml`.

---

## 🏗️ GH Definition Builder (NEW)

Programmatically create Grasshopper definitions with Python script components.
The full pipeline: **Generate Code → Build .gh → Deploy to Compute Platform → Solve via API**

### Build a Definition via RhinoClaw

```bash
# Build a .gh file with inputs + Python script
python3 ghscript.py build \
  --name "ParametricBox" \
  --script my_script.py \
  --inputs inputs.json \
  --output "C:/temp/gh_definitions/ParametricBox.gh"
```

### Build + Deploy to Rhino Compute Platform

```bash
# Build .gh and deploy to ~/projects/rhino-compute-platform/definitions/
python3 ghscript.py deploy \
  --name "ParametricBox" \
  --script my_script.py \
  --inputs inputs.json
```

After deploy, the definition is immediately solvable:
```
POST http://localhost:8100/solve
{ "definition": "ParametricBox.gh", "inputs": { "Width": 200, "Height": 100 } }
```

### Input Spec Format (inputs.json)

```json
[
  { "name": "Width",  "type": "number",  "default": 200, "min": 10, "max": 1000 },
  { "name": "Height", "type": "number",  "default": 100, "min": 10, "max": 500 },
  { "name": "Count",  "type": "integer", "default": 5,   "min": 1,  "max": 20 },
  { "name": "Label",  "type": "string",  "default": "Part-A" },
  { "name": "Mirror", "type": "boolean", "default": false }
]
```

### GHPython Script Template

The script receives inputs as variables matching the input names:

```python
# Inputs: Width, Height (injected by Grasshopper)
# Output: Geometry (assigned to 'a' output)
import Rhino.Geometry as rg

plane = rg.Plane.WorldXY
box = rg.Box(plane, rg.Interval(-Width/2, Width/2), 
             rg.Interval(-Height/2, Height/2), 
             rg.Interval(0, Height))
Geometry = box.ToBrep()
```

### Execute Python Directly in Rhino

```bash
# Quick test without building a GH definition
python3 ghscript.py exec --code "import Rhino; print(Rhino.RhinoApp.Version)"
python3 ghscript.py exec --file my_script.py
```

### How It Works

1. `build_gh_definition` command in RhinoClaw creates a GH document with:
   - Number Sliders / Boolean Toggles / Panels for each input
   - A Python 3 Script component with the provided code
   - Wired connections between inputs and script
2. The document is saved as binary `.gh` file
3. `deploy` copies to Compute Platform `definitions/` and writes `.meta.json`
4. `/solve` endpoint picks it up automatically

---

## 📜 RhinoScript Execution

```bash
# Execute inline code
python3 script_exec.py -c "import rhinoscriptsyntax as rs; rs.AddSphere([0,0,0], 10)"

# Execute script file
python3 script_exec.py -f ~/scripts/my_script.py
```

---

## 🔍 Log Monitoring

Check the Rhino log for debugging (requires Windows filesystem access / TOTP):

```bash
# View recent log entries (needs TOTP unlock for /mnt/c access)
tail -30 "/mnt/c/Users/YOUR_USERNAME/AppData/Local/Temp/rhinoclaw.log"

# Alternative: use rhino_client to query logs via TCP
python3 rhino_client.py get_logs
```

---

## Example: Complete PBR Scene Workflow

```bash
# 1. Create layer with material
python3 layers.py create "Gold_Parts" --color 255,215,0
python3 materials.py preset gold
# → Note material_id

# 2. Assign material to layer
python3 materials.py assign "Gold_Parts" <material_id>
python3 layers.py set "Gold_Parts"

# 3. Create geometry
python3 geometry.py sphere --radius 5 --name "Gold_Ball"
python3 geometry.py box --width 10 --length 10 --height 2 --position 0,0,-3

# 4. Boolean difference (cut hole)
python3 geometry.py cylinder --radius 2 --height 5 --position 0,0,-3
python3 booleans.py difference <box_id> <cylinder_id>

# 5. Set camera and capture
python3 viewport.py camera --position 30,30,20 --target 0,0,0 --lens 35
python3 viewport.py screenshot --width 1920 --height 1080
# → Returns linux_path, read directly with Read tool
```

---

## ⚠️ Error Handling

The `rhino_client.py` provides custom exceptions for robust error handling:

| Exception | When |
|-----------|------|
| `RhinoConnectionError` | Can't connect or connection lost |
| `RhinoTimeoutError` | No response within timeout |
| `RhinoCommandError` | Rhino returned an error |
| `ValidationError` | Invalid parameters |

**Auto-retry:** The client has a `@with_retry` decorator for automatic reconnection with exponential backoff (default: 3 retries).

**Context Manager:** Use `with RhinoClient() as client:` for automatic connect/disconnect.

---

## 🏗️ VisualARQ BIM Objects (OPTIONAL)

Control VisualARQ BIM objects (walls, doors, windows, columns, beams, etc.). 

> **Note:** VisualARQ is an optional add-on. All commands gracefully degrade if not installed - no crashes or errors.

### Check Availability

```bash
# Check if VisualARQ is installed
python3 visualarq.py check

# Get available styles, levels, and buildings
python3 visualarq.py info
```

### Walls

```bash
# Create a wall
python3 visualarq.py wall --style "Generic - 200mm" \
  --start 0,0,0 --end 10,0,0 --height 3.0 \
  --layer "Walls" --name "ExtWall_01"

# List available wall styles
python3 visualarq.py wall-styles

# Add a new wall style
python3 visualarq.py add-wall-style --name "Custom 300mm" --width 0.3
```

### Doors & Windows

```bash
# Create a door (requires existing wall)
python3 visualarq.py door --style "Single Swing" \
  --wall-id <wall_guid> --position 0.5 \
  --width 0.9 --height 2.1 --name "MainEntry"

# Create a window
python3 visualarq.py window --style "Fixed" \
  --wall-id <wall_guid> --position 0.3 \
  --width 1.2 --height 1.5 --name "Window_01"

# List available styles
python3 visualarq.py door-styles
python3 visualarq.py window-styles
```

**Position Parameter:** 0.0 = start of wall, 1.0 = end of wall, 0.5 = middle

### Structural Elements

```bash
# Create a column
python3 visualarq.py column --style "Rectangular" \
  --position 0,0,0 --height 3.0 --name "Col_A1"

# Create a beam
python3 visualarq.py beam --style "Rectangular" \
  --start 0,0,3 --end 5,0,3 --name "Beam_B1"

# Create a slab (requires boundary curves)
python3 visualarq.py slab --boundary <curve_id1>,<curve_id2> \
  --thickness 0.25 --name "Slab_01"
```

### Levels & Buildings

```bash
# List all levels
python3 visualarq.py levels

# Add a new level
python3 visualarq.py add-level --name "OG1" --elevation 3.0

# Add a building
python3 visualarq.py add-building --name "Haus A"
```

### Custom BIM Parameters

```bash
# Add a custom parameter to an object
python3 visualarq.py add-param --name "FireRating" --type text \
  --object-id <guid>

# Set parameter value
python3 visualarq.py set-param --name "FireRating" \
  --value "EI30" --object-id <guid>

# Get parameter value
python3 visualarq.py get-param --name "FireRating" --object-id <guid>
```

**Parameter Types:** `text`, `number`, `integer`, `boolean`, `length`

### IFC Import/Export

```bash
# Export to IFC
python3 visualarq.py ifc-export --path "output.ifc" --version "IFC4"

# Import IFC file
python3 visualarq.py ifc-import --path "model.ifc"
```

**Supported IFC Versions:** `IFC2x3`, `IFC4`, `IFC4.3`

### Query VisualARQ Objects

```bash
# List all walls with properties
python3 visualarq.py list-walls

# List all doors with properties
python3 visualarq.py list-doors

# List all windows
python3 visualarq.py list-windows

# Overview of all VisualARQ objects by type
python3 visualarq.py list-objects
```

### Example: Complete BIM Workflow

```bash
# 1. Check if VisualARQ is available
python3 visualarq.py check
# → {"available": true, "version": "detected"}

# 2. Create building structure
python3 visualarq.py add-building --name "Office Building"
python3 visualarq.py add-level --name "Ground Floor" --elevation 0.0
python3 visualarq.py add-level --name "First Floor" --elevation 3.5

# 3. Create walls
python3 visualarq.py wall --style "Generic - 200mm" \
  --start 0,0,0 --end 10,0,0 --height 3.0 --name "SouthWall"
# → Note wall_id for door/window insertion

# 4. Add openings
python3 visualarq.py door --style "Single Swing" \
  --wall-id <wall_id> --position 0.7 \
  --width 0.9 --height 2.1 --name "MainEntry"

python3 visualarq.py window --style "Fixed" \
  --wall-id <wall_id> --position 0.3 \
  --width 1.5 --height 1.2 --name "SouthWindow"

# 5. Add custom BIM data
python3 visualarq.py add-param --name "FireRating" --type text \
  --object-id <wall_id>
python3 visualarq.py set-param --name "FireRating" \
  --value "EI90" --object-id <wall_id>

# 6. Export to IFC
python3 visualarq.py ifc-export --path "office_building.ifc" --version "IFC4"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Connection refused | Run `tcpstart` in Rhino command line |
| Timeout | Increase timeout in config.json (max 120s) |
| Boolean failed | Ensure objects are closed solids (Breps) |
| Screenshot path issues | Check windows_dir UNC path in config |
| Command not found | Rebuild plugin after C# changes |
| Objects on wrong layer | Set layer first with `layers.py set "LayerName"` |
| PBR material not visible | Materials use RenderMaterials table (fixed in 0.1.3.7+) |
| Script timeout | Use `--timeout 60` for large scripts |
| `RhinoConnectionError` | Auto-retry is built in (3 attempts), check if plugin running |
| VisualARQ not available | Install VisualARQ plugin or gracefully ignore VA commands |
