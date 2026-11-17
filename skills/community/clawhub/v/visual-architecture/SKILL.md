---
name: visual-architecture
description: "Create deterministic, local-first architecture artifacts from typed JSON or TypeScript-aware repo extraction: validate specs, render SVG/HTML diagrams, and emit source-backed receipts agents can cite."
metadata:
  version: "1.8.3"
---
# Visual Architecture

Create architecture artifacts with the bundled Python renderer instead of hand-writing SVG. v1.8 adds a public TypeScript-monorepo case study path on top of the v1.7 extraction engine: source-backed case-study docs, generated artifacts, README quick-starts, and gallery conversion proof.

Use this when the user needs a trustworthy system map, agent workflow, sequence, data-flow, lifecycle/state diagram, repo-evidence diagram, or PR delta review sketch that should stay local, deterministic, and reviewable.

## Workflow

1. Either extract a TypeScript-aware starter spec from a repo or create a JSON file with `mode`, `title`, `nodes`, and `edges`.
   - Supported modes: `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle`, `pr-delta`.
   - Supported themes: `classic` for documentation, `showcase` for README/release proof images.
2. Snap intended node positions to the renderer grid mentally before writing them:
   - horizontal grid: 120px
   - vertical grid: 80px
3. For repo-aware drafts, extract and layout first:

```bash
python3 skills/visual-architecture/scripts/render_architecture.py extract-repo . --output repo-map.json --title "Generated Repo Map"
python3 skills/visual-architecture/scripts/render_architecture.py layout repo-map.json repo-map.layout.json --mode architecture
```

4. Validate first:

```bash
python3 skills/visual-architecture/scripts/render_architecture.py validate input.json --json
```

5. Deliver the final artifact with a receipt:

```bash
python3 skills/visual-architecture/scripts/render_architecture.py deliver input.json output.html --json
```

Use `.svg` for a static docs artifact or `.html` for a self-contained presentation artifact.

For PR delta review, either extract a PR concern map from git refs or compare two specs:

```bash
python3 skills/visual-architecture/scripts/render_architecture.py extract-pr --base origin/master --head HEAD --output pr-delta.json
python3 skills/visual-architecture/scripts/render_architecture.py compare base.json head.json pr-delta.html --spec pr-delta.json --json
```

6. If `rsvg-convert` is available and you need a bitmap preview, run:

```bash
rsvg-convert -o output.png output.svg
```

## JSON Input Structure

```json
{
  "title": "Service Map",
  "mode": "architecture",
  "theme": "classic",
  "summary": "One local request path with async work and model access.",
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
- `theme`: set `showcase` on the top-level spec for dark public-facing artifacts
- `evidence`: object or list with `source`, optional `line`/`lines`, `commit`, `confidence`, and `note`

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

- Validate rejects unsupported node/edge kinds and unknown edge endpoints before rendering
- Deliver writes the artifact atomically and emits a JSON receipt with SHA-256 hashes
- Validation receipts include a quality score for spacing, density, route crossings, and visual overlap
- `extract-repo`, `layout`, `extract-pr`, and `bundle` turn repo evidence into checked artifacts without hand-placing every node
- `--min-quality` can fail delivery or bundle export when the artifact is not presentation-grade
- The generated gallery can load spec/receipt JSON and show story steps plus source evidence
- Evidence badges render as `SRC n` on nodes with source-backed evidence
- PR delta compare writes added/removed node and edge facts into the receipt
- Route arrows orthogonally only
- Render in this order: background, arrows, nodes, labels
- Keep label shields behind arrow text for readability
- Stay restrained: clean strokes, no decorative effects, and hide the editing grid unless explicitly requested

## Usage Notes

- Prefer this skill when the user wants architecture diagrams, routing maps, or system relationship visuals.
- Choose semantic kinds first, then place nodes on the grid, then add only the edges needed to explain flow.
- Keep diagrams sparse. If a diagram feels crowded, split it into two files instead of forcing a dense composite.
- Prefer `deliver` for handoff. A passing render without a receipt is a draft.
- Do not claim repository evidence unless the spec names source files, commits, or confidence explicitly.

## Example

Use `examples/service-map.json` as a generic architecture starting point. Use `examples/agent-runtime.json`, `examples/sequence-cache-miss.json`, `examples/dataflow-analytics.json`, and `examples/lifecycle-agent-task.json` for the non-architecture modes. Use `examples/repo-evidence-map.json` for source-pinned evidence, and `examples/pr-delta-before.json` plus `examples/pr-delta-head.json` for generated PR deltas.
