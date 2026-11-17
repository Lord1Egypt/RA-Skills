# Diagnostics

`visual-architecture validate --json` and `deliver --json` return stable diagnostic codes. The validator is intentionally local and conservative: it checks authored JSON facts and renderer-safe geometry, not live infrastructure.

## Spec Codes

- `spec.type` - input is not a JSON object
- `mode.unsupported` - `mode` is not one of the supported diagram modes
- `title.required` - title is missing or empty
- `nodes.required` - nodes are missing or empty
- `edges.type` - edges exists but is not a list

## Node Codes

- `node.type` - node is not an object
- `node.id.required` - node id is missing or empty
- `node.id.duplicate` - node id repeats
- `node.label.required` - node label is missing or empty
- `node.kind.unsupported` - node kind is not renderer-supported
- `node.x.required` / `node.y.required` - coordinate is missing or non-numeric
- `node.x.snapped` / `node.y.snapped` - coordinate will snap to the renderer grid
- `node.position.shared` - two nodes share one grid position

## Edge Codes

- `edge.type` - edge is not an object
- `edge.from.unknown` / `edge.to.unknown` - endpoint id does not exist
- `edge.kind.unsupported` - edge kind is not renderer-supported
- `edge.label.long` - label may crowd the route
- `edge.via.type` - via point is not an object
- `edge.via.x.required` / `edge.via.y.required` - via coordinate is missing or non-numeric
- `edge.via.x.snapped` / `edge.via.y.snapped` - via coordinate will snap to the renderer grid
- `edge.route.crosses-node` - an edge route crosses an unrelated node box

## Evidence Codes

- `evidence.type` - evidence is not an object or list
- `evidence.item.type` - evidence list item is not an object
- `evidence.source.required` - evidence source is missing
- `evidence.line.type` - evidence line is not an integer
- `evidence.lines.type` - evidence lines are not `[start, end]` integers
- `evidence.commit.type` - evidence commit is not a string
- `evidence.confidence.unknown` - confidence is not `high`, `medium`, or `low`

## Visual Quality Diagnostics

- `quality.node.overlap` - rendered node boxes overlap or sit too close to be presentation-grade.
- `quality.node.spacing` - node centers are too close for a clean artifact.
- `quality.route.crossings` - unrelated edge routes cross and should be rerouted with `via` points.
- `quality.route.complex` - an edge route has enough turns to become visually noisy.
- `quality.density.high` - the artifact is dense enough that it should probably be split or narrated as a smaller story.

Receipts expose `validation.metrics.quality.score` and `validation.metrics.quality.rating`. Treat `needs-work` and `poor` as visual defects even when the JSON shape is valid.
