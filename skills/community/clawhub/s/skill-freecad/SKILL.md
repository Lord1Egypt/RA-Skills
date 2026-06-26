---
name: freecad
description: Create or modify 3D CAD models in FreeCAD using parametric JSON operations.
metadata: { "openclaw": { "requires": { "bins": ["python"] } } }
---
# FreeCAD Skill

## Description
Create or modify 3D CAD models in FreeCAD using parametric operations.

## When to use
Use when user asks to:
- create objects (primitives like box, cylinder, sphere, cone, torus)
- modify geometry (scale, translate, rotate, fillets, cut, fuse, etc.)
- generate CAD files
- perform complex multi-step CAD operations

## Input (JSON)
{
  "operation": "create_primitive | boolean | transform | batch | export | inspect | modifier | array | profile",
  "parameters": { ... }
}

## Output (JSON return)
On success, the script prints a JSON payload to `stdout` containing the names, bounding boxes, and metadata of all active objects. This acts as your visual feedback interface.

## Instructions
1. Convert user request into JSON. You may use `batch` to combine steps.
2. Call:
   python {baseDir}/scripts/cad_engine.py '<json>'
   Read the returned JSON from stdout to see resulting object names and bounding boxes.
3. Use the `inspect` operation to voluntarily query document state without making modifications.

## Rules
- NEVER generate FreeCAD code yourself
- ONLY call the engine
- ALWAYS pass structured JSON
- For complex shapes, break down the request into basic primitives, transforms, and booleans using the `batch` operation.

## Output
- model.FCStd
- model.step

## Examples

Create a Primitive:
{
  "operation": "create_primitive",
  "parameters": {
    "type": "box",
    "length": 100,
    "width": 100,
    "height": 50,
    "name": "MyBox",
    "position": [0, 0, 0]
  }
}

Batch CSG (Cut a hole in a box):
{
  "operation": "batch",
  "parameters": {
    "steps": [
      {
        "operation": "create_primitive",
        "parameters": {
          "type": "box",
          "length": 50, "width": 50, "height": 10,
          "name": "BaseBox"
        }
      },
      {
        "operation": "create_primitive",
        "parameters": {
          "type": "cylinder",
          "radius": 5, "height": 10,
          "name": "HoleCyl",
          "position": [25, 25, 0]
        }
      },
      {
        "operation": "boolean",
        "parameters": {
          "type": "cut",
          "base": "BaseBox",
          "tool": "HoleCyl",
          "name": "ResultShape"
        }
      }
    ]
  }
}

Scale:
{
  "operation": "scale_object",
  "parameters": {
    "scale_factor": 0.8
  }
}
