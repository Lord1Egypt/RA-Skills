# GH Script Templates

Pre-built GHPython scripts for common parametric objects.
Each template has a `.py` (script) and `.inputs.json` (parameter definitions).

## Available Templates

| Template | Description | Inputs |
|----------|-------------|--------|
| `parametric_box` | Box with optional filleted edges | Width, Height, Depth, FilletRadius |
| `door_frame` | Parametric Türzarge (door frame) | Lichthoehe, Lichtbreite, Zargen, Falz |

## Usage

### Via RhinoClaw (interactive, live in Rhino)

```bash
cd ~/clawd/skills/rhinoclaw/scripts
python3 ghscript.py build \
  --name "ParametricBox" \
  --script ../templates/ghscripts/parametric_box.py \
  --inputs ../templates/ghscripts/parametric_box.inputs.json
```

### Via Rhino Compute Platform (headless, browser viewer)

```bash
python3 ghscript.py deploy \
  --name "ParametricBox" \
  --script ../templates/ghscripts/parametric_box.py \
  --inputs ../templates/ghscripts/parametric_box.inputs.json
```

Then open the Compute Platform viewer and select the definition.

## Writing New Templates

### Script Rules (GHPython / RhinoCommon)

1. Inputs are injected as global variables (matching input names)
2. Output variables must match the output names (default: `Geometry`)
3. Use `Rhino.Geometry` namespace for all geometry
4. Return Brep/Mesh for best Compute compatibility
5. Lists work too – assign a Python list to the output

### Input Types

- `number` → `GH_NumberSlider` (float, with min/max/step)
- `integer` → `GH_NumberSlider` (integer mode)
- `boolean` → `GH_BooleanToggle`
- `string` → `GH_Panel`

### Example Workflow

```
Agent: "Build a parametric shelf with 3 shelves, adjustable width and height"

1. Agent writes shelf.py (RhinoCommon geometry)
2. Agent writes shelf.inputs.json (Width, Height, ShelfCount, Thickness)
3. Agent calls: ghscript.py deploy --name "ParametricShelf" --script shelf.py --inputs shelf.inputs.json
4. User opens Compute Platform viewer → adjusts sliders → exports STL for CNC
```
