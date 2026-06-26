---
name: visual-architecture
description: "Render restrained architecture diagrams from structured JSON with a deterministic local SVG renderer."
metadata:
  version: "0.2.5"
---
# Visual Architecture

Render architecture diagrams with the bundled Python renderer instead of hand-writing SVG.

## Workflow

1. Create a JSON file with `title`, `nodes`, and `edges`.
2. Snap intended node positions to the renderer grid mentally before writing them:
   - horizontal grid: 120px
   - vertical grid: 80px
3. Run:

```bash
python3 skills/visual-architecture/scripts/render_architecture.py input.json output.svg
```

4. If `rsvg-convert` is available and you need a bitmap preview, run:

```bash
rsvg-convert -o output.png output.svg
```

## JSON Input Structure

```json
{
  "title": "Service Map",
  "nodes": [
    {
      "id": "web",
      "label": "Web App",
      "subtitle": "User interface",
      "kind": "service",
      "x": 120,
      "y": 160
    },
    {
      "id": "api",
      "label": "API",
      "subtitle": "Business logic",
      "kind": "service",
      "x": 360,
      "y": 160
    }
  ],
  "edges": [
    {
      "from": "web",
      "to": "api",
      "kind": "primary-data",
      "label": "HTTP"
    }
  ]
}
```

## Node Kinds

- `service`: rounded rectangle
- `llm`: double-border rounded rectangle
- `agent`: hexagon
- `memory`: cylinder

Each node requires:
- `id`: unique string
- `label`: primary title
- `kind`: one of the node kinds above
- `x`, `y`: grid-aligned center coordinates

Optional:
- `subtitle`: smaller secondary label
- `show_grid`: set true to display the editing grid in the exported SVG

## Edge Kinds

- `primary-data`: blue solid arrow
- `memory-write`: green dashed arrow
- `control`: slate dashed arrow

Each edge requires:
- `from`: source node id
- `to`: target node id

Optional:
- `label`: rendered on the route with a shielding background rect
- `source_side`, `target_side`: force edge anchors (`left`, `right`, `top`, `bottom`)
- `via`: array of orthogonal turn points, each with `x` and `y`
- `label_segment`: zero-based segment index to place the label on
- `label_offset`: `[dx, dy]` shift for fine label placement

## Renderer Guarantees

- Route arrows orthogonally only
- Render in this order: background, arrows, nodes, labels
- Keep label shields behind arrow text for readability
- Stay restrained: clean strokes, no decorative effects, and hide the editing grid unless explicitly requested

## Usage Notes

- Prefer this skill when the user wants architecture diagrams, routing maps, or system relationship visuals.
- Choose semantic kinds first, then place nodes on the grid, then add only the edges needed to explain flow.
- Keep diagrams sparse. If a diagram feels crowded, split it into two files instead of forcing a dense composite.

## Example

Use `examples/service-map.json` as a generic starting point for web app, API, worker, database, and LLM provider diagrams.
