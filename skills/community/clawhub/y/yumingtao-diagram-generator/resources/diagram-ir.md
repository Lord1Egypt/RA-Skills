# Diagram IR

Diagram IR is the shared planning structure used before rendering. Agents must build and embed this model before producing HTML/SVG, draw.io XML, or any future export format.

The IR serves two purposes:
1. **Planning**: prevents duplicated diagram logic by giving the same actors, regions, nodes, edges, and notes to multiple renderers.
2. **Revise anchor**: the IR is embedded in the generated artifact inside `<script type="application/json" id="diagram-ir">`. The revise workflow reads this slot first to reconstruct the planning model — enabling targeted field edits rather than full SVG re-reading.

## Revise Workflow Entry Point

When entering revise mode on an existing artifact:
1. **Read `#diagram-ir` slot first.** If the `<script type="application/json" id="diagram-ir">` element exists, parse it as the authoritative IR. Apply the requested edit to the IR fields, then re-render only the affected regions.
2. **Fallback (legacy artifacts).** If the slot is absent, fall back to reading the SVG directly to reconstruct the IR. After saving, write the reconstructed IR into the slot so the artifact is upgraded for future revisions.

## Top-Level Shape

```yaml
title: Commerce Platform System Map
lens: system
scope: production request, identity, data, event, and telemetry paths
language: en
mode: create
canvas:
  complexity: standard
  viewBox: "0 0 1500 900"
regions: []
nodes: []
edges: []
notes: []
assumptions: []
edit_scope: null
```

`mode` is `create` for a new artifact and `revise` when editing an existing one. When `mode: revise`, set `edit_scope` to a short phrase such as `layout-only`, `content update`, `connector cleanup`, or `add one component without redesign`.

## Regions

Regions describe ownership, runtime, trust, infrastructure, or data-contract areas.

```yaml
- id: runtime
  label: Production Runtime Boundary
  role: infrastructure
  bounds: { x: 360, y: 100, width: 850, height: 570 }
  contains: [gateway, core_services, database, event_bus]
```

Required fields:

- `id`: stable identifier
- `label`: visible region label
- `role`: `infrastructure`, `trust`, `runtime`, `data`, `operations`, or `process`
- `bounds`: approximate SVG rectangle
- `contains`: node IDs when known

## Nodes

Nodes are the visible entities in the map.

```yaml
- id: core_services
  label: Core Services
  role: compute
  responsibility: user, catalog, order, and payment APIs
  technology: Kubernetes pods
  bounds: { x: 830, y: 235, width: 170, height: 130 }
```

Supported roles:

- `actor`
- `entry`
- `compute`
- `state`
- `message`
- `control`
- `telemetry`
- `external`

Node labels should be short. Move long details into `responsibility`, `technology`, notes, or assumptions.

## Edges

Edges describe movement or control between nodes.

```yaml
- id: client_to_gateway
  from: clients
  to: gateway
  kind: sync
  label: HTTPS
  role: entry
  route: orthogonal
  labelAnchor: { x: 296, y: 286, width: 46 }
```

Optional `labelAnchor` records where the connector label sits: `x`/`y` is the label's anchor point (baseline for SVG text) and `width` its estimated box (`chars × per-glyph × font-size + 16`). When present, `check-diagram.mjs` verifies the label box does not overlap any node rectangle; when absent, label placement stays a render-time concern.

Supported `kind` values:

- `sync`: request, response, direct API call, or direct read/write
- `async`: queue, topic, stream, deferred worker, callback
- `control`: identity, policy, secret, admin, authorization
- `telemetry`: logs, metrics, traces, audits, health events
- `replication`: data copy, ETL, synchronization, indexing

Use `role` to select connector color. Connector arrowheads must match connector stroke color.

Edge direction must follow the real dependency. When one node only *consults* another (a registry, lookup table, policy store, or config), model it as a chain — `registry → engine → target` — not as two edges both ending at the target. Drawing both at the target falsely implies two independent gates.

## Layout Bookkeeping

Before emitting connectors and labels, keep a bounds registry of every node's rectangle (`x, y, width, height`). Use it to guarantee, by construction, that:

- each connector's endpoint lands on a target node's edge (not in empty space),
- each label's estimated bounding box overlaps no node rectangle,
- each region title clears the boxes to its right,
- sibling nodes in the same lane have intentional gutter spacing,
- fan-out branches have planned branch points instead of ad hoc bends.

This registry is what the renderer checks during the render-and-inspect pass. Semantic fidelity matters more than decoration, but a label hidden behind a box loses fidelity too.

## Notes

Notes become the right-side notes rail in HTML/SVG and metadata in other renderers.

```yaml
- title: System Shape
  bullets:
    - Clients enter through edge controls before reaching private services.
    - Durable state is split across transactional, cache, event, and object surfaces.
```

Default note titles:

- `System Shape`
- `Critical Flows`
- `Operational Notes`

## Assumptions

Assumptions record inferred details that are not explicit in the prompt.

```yaml
- The API gateway performs token validation before forwarding traffic.
- Kafka topics are retained long enough for notification retry handling.
```

Put assumptions in notes instead of cluttering node labels.

## Renderer Contract

Every renderer should preserve:

- title, lens, and scope
- region grouping
- node role and label
- edge direction, kind, and label
- notes and assumptions

Renderers may simplify visual effects. Semantic fidelity matters more than exact decoration.
