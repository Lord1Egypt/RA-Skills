# Diagram Generator Rules

## Intent

Create a self-contained engineering map that lets a reader answer five questions quickly:

- Who enters the system?
- Which runtime owns each responsibility?
- Where does data become durable?
- Which paths are synchronous, asynchronous, or privileged?
- What must operators watch when the system is running?

The output is a standalone HTML document with inline SVG. It should be useful in architecture reviews, onboarding notes, incident writeups, and implementation handoffs.

## Generation Workflow

1. Normalize the brief into actors, runtimes, responsibilities, stores, messages, control points, external dependencies, and risks.
2. If the task is an edit to an existing diagram, inspect the current HTML/SVG first and preserve unchanged story elements, notes, color semantics, and unrelated flows. Do not regenerate from scratch unless the user asks for a redesign or the existing file is unusable.
3. Select one lens: system, implementation, infrastructure, trust, data movement, deployment, or process.
4. Draft Diagram IR using `resources/diagram-ir.md`: title, lens, scope, regions, nodes, edges, notes, assumptions, and edit scope when revising an existing artifact. Embed the final IR as JSON in `<script type="application/json" id="diagram-ir">` before the closing `</body>` tag.
5. Merge tiny implementation details into named capabilities unless the user asks for file-level traceability.
6. Choose a canvas size from the density rules below.
7. Plan every node box first and record its rectangle (`x, y, width, height`) in a bounds registry. Then draw the SVG in layers: stage regions, connectors, connector labels, components, map key. Components render after connectors so node fills mask lines that pass behind them.
8. Route connectors and position every label against the bounds registry, so no label overlaps a box and every arrow lands on a node edge (see Connector Rules and Label and Text Placement).
9. When revising an existing diagram, prefer the smallest coordinate and path changes that fix spacing, alignment, clipping, or routing defects. Keep identifiers, copy, and stable geometry unless the requested change requires more.
10. Fill the notes rail with System Shape, Critical Flows, and Operational Notes unless the user asks for different sections.
11. Render the complete HTML artifact to a raster image, look at the picture, and fix any overlap, clipped text, or arrow that misses its target — then re-render until clean. Prefer headless Chrome/Chromium, Playwright, or OS preview/Quick Look because they cover the map, toolbar, and notes rail together. `rsvg-convert` or ImageMagick may be used only for an extracted SVG canvas and do not replace full-page HTML inspection. If no renderer is available, say so and inspect coordinates against the bounds registry instead.
12. Run `node scripts/check-diagram.mjs <output-file.html>` before returning the file. If the checker exits with errors, fix the reported issues (update the IR, correct the SVG, fill placeholders) and re-run until it passes. Only then return the artifact. If the script is unavailable in the current environment, fall back to the manual release check below and note the skip.

## Existing Diagram Revision Mode

Use this mode when the user supplies an existing HTML/SVG map or asks to improve a diagram already generated.

1. **Read the IR slot first.** Look for `<script type="application/json" id="diagram-ir">` in the artifact and parse it as the authoritative planning model. If the slot exists, update the relevant IR fields for the requested change and re-render only the affected regions — do not re-read the full SVG unless a node's geometry must change. If the slot is absent (legacy artifact), fall back to reading the current SVG to reconstruct the IR, then write the reconstructed IR into the slot when saving so the artifact is upgraded.
2. Identify the exact requested edit scope: content, layout, connectors, notes, canvas size, or visual polish.
3. Preserve all unrelated components, labels, notes sections, and semantic colors.
4. Prefer local edits over wholesale regeneration. If three or fewer components are changing, keep the rest of the coordinates stable unless they block readability.
5. If the defect is layout-only, do not rewrite narrative text or rename nodes.
6. If the defect is content-only, do not introduce a new visual structure unless the old one fails the layout rules.
7. If revision introduces a new connector color, add a matching `<marker>` definition in `<defs>` before using its `marker-end` URL.
8. Re-check the edited diagram against the same bounds registry and release check as a fresh diagram.

## Revision Cookbook

Use these decision rules for common revision tasks:

### Add One Component To An Existing Region

- If the new component semantically belongs to an existing region, expand that region first.
- Prefer extending the region or canvas over compressing established gutters.
- Keep unrelated regions stable unless the new footprint would cause overlap or clipping.

### Add A New Region

- Prefer expanding the canvas and appending the new region at the bottom or right edge that matches the dominant reading path.
- Avoid shrinking existing regions just to make room unless the user asked for a denser redesign.

### Decide Whether To Resize The Canvas

- In revise mode, compare the current component count and region count with the original complexity tier.
- If the revised diagram exceeds the original tier by two or more visible components, move to the next canvas tier before re-spacing nodes.
- Also expand the canvas when a map key, region title, or notes-related boundary would otherwise be clipped.

### Shared-Trunk Fan-Out Labels

- For a shared-trunk fan-out, place one label on the trunk segment.
- Do not repeat the same label on each branch unless each branch carries a different meaning.

## Diagram Lenses

### System Lens

Use for service relationships, user entry points, storage ownership, external integrations, and operational context. Prefer capability labels over code names.

### Implementation Lens

Use for repository-derived maps, script execution chains, generated artifacts, scheduled jobs, and handoff contracts. Group concrete files into 3-6 meaningful stages instead of drawing a file inventory.

### Infrastructure Lens

Use for regions, clusters, networks, gateways, managed services, object stores, queues, containers, serverless functions, and deployment placement.

### Trust Lens

Use for identity providers, public/private boundaries, privileged operations, secrets, policy checks, token validation, and administrative paths.

### Data Movement Lens

Use for ingestion, replication, event streams, durable records, transformations, search indexes, exports, and reporting.

### Process Lens

Use for ordered interactions, approval chains, incident response, automation pipelines, and sequence-like flows.

## Visual System

Use the template's "atlas" style: a light document surface, a muted canvas, crisp ink labels, and restrained semantic accents. Do not recreate a dark dashboard unless the user explicitly requests one.

| Semantic role | Stroke | Fill | Typical use |
| --- | --- | --- | --- |
| Actor | `#0f766e` | `#ccfbf1` | Users, clients, CLI, input producers |
| Entry | `#2563eb` | `#dbeafe` | CDN, WAF, ingress, API gateways |
| Compute | `#15803d` | `#dcfce7` | APIs, services, workers, jobs |
| State | `#7c3aed` | `#ede9fe` | Databases, caches, object stores, indexes |
| Message | `#c2410c` | `#ffedd5` | Queues, topics, streams, async buses |
| Control | `#be123c` | `#ffe4e6` | Identity, policy, secrets, privileged actions |
| Telemetry | `#a16207` | `#fef3c7` | Logs, metrics, traces, alerts, audits |
| External | `#475569` | `#f1f5f9` | Partner systems, SaaS APIs, third parties |

Use solid connectors for request/response or data writes, dashed connectors for async, telemetry, audit, or policy side paths. Connector arrowheads must use the same color as their connector stroke.

## Component Grammar

- Component boxes use a compact label stack: name, responsibility, optional technology.
- Stage regions use low-contrast filled rectangles with a short label at the top-left.
- Trust or policy regions use a red/pink outline and light fill.
- Data stores should include a small cylinder cue or a "state" tag.
- Queues and streams should look like horizontal channels or capsule bars.
- External dependencies sit outside the main runtime region when space allows.
- The map key should explain semantic roles and connector line types.

## Layout Rules

- Pick a dominant reading path: left-to-right for request/data systems, top-to-bottom for process flows.
- Place actors before entry controls, entry controls before compute, compute before state or message channels.
- Keep stores close to the capabilities that own or mutate them.
- Keep observability and audit surfaces visually cross-cutting, usually along the bottom or in a side band.
- Keep external systems outside the main runtime boundary unless they are hosted by the same platform.
- Prefer 4-7 meaningful components in the main path. Move secondary details into grouped regions or the notes rail.
- Keep labels short enough to fit inside nodes. Use notes for assumptions and long explanations.
- Use consistent gutters between sibling boxes in the same lane. A visible jump in spacing is a defect unless it encodes a deliberate boundary.
- Keep vertical gutters between adjacent rows or stacked regions consistent within about 5px unless the extra space encodes a deliberate boundary.
- **Nodes must sit inside their region frame with breathing room.** A node listed in a region's `contains` keeps at least 10px of clear gutter on every side — the checker enforces this floor. A node flush with the region border makes the two strokes paint on top of each other and reads as a broken frame. Widen the region or shrink the node before letting edge coordinates drive the layout.
- Center related lanes and child groups visually within their parent region. Do not leave a large dead band above or below one subsection while adjacent sections are dense.
- When adding a new row or column to an existing diagram, rebalance neighboring nodes instead of only appending into leftover space.
- Reserve clear gutters for connector labels and branch points before finalizing box positions.

## Canvas Density

Choose the SVG viewBox after estimating node count and region count:

| Complexity | Use when | Suggested viewBox |
| --- | --- | --- |
| Compact | 4-7 components, 1-2 regions | `0 0 1280 760` |
| Standard | 8-13 components, 2-4 regions | `0 0 1500 900` |
| Wide | 14-20 components, 3-6 regions | `0 0 1760 1020` |
| Process | 6-12 ordered steps | `0 0 1320 920` |

Reserve a band of at least 56px from the lowest component's bottom edge to the viewBox bottom, and the map key must fit entirely inside that band. Increase height before drawing if a region, key, or label would be clipped.

## Connector Rules

- Route connectors with simple horizontal/vertical segments whenever possible.
- Stop connectors at node edges, not at text centers.
- **A connector must not pass through any node rectangle.** Route orthogonal segments around obstacles using the clear channels between rows and columns; if no channel exists, widen the gap or expand the canvas rather than letting a line cross a box. The checker enforces this: every segment of every connector path is tested against every node's bounds (except the connector's own source and target). A segment that penetrates a box's interior fails the build.
- **Reserve routing channels, then place boxes.** Treat the gaps between node columns and rows as dedicated connector corridors (the system-map equivalent of sequence-diagram lifelines). Lay out boxes so the vertical and horizontal strips between them stay clear; run connectors inside those strips. Never let a box expand into an existing channel — move the box or widen the canvas first. A connector corridor must be wide enough that every segment inside it keeps at least 3px clearance from every node and region border; a line that grazes a box or runs along a region edge reads as a merged/double line and is rejected by the checker.
- Every connector must begin and end **on a node edge**: the final point's `x` equals the target's left or right edge, or its `y` equals the target's top or bottom edge (account for the arrowhead `refX` so the tip touches the border). An arrowhead that stops in empty canvas is a defect — extend it to the box or delete the connector.
- Draw control, policy, and dependency edges in the **real direction of dependence**. If component A consults component B (a registry, lookup table, policy store, or config), draw the chain `B → A → target`, not two parallel arrows both pointing at the target. Parallel fans imply two independent gates where there is really one.
- Place connector labels near the middle of the route with a small background pill when the line crosses a busy area.
- Avoid more than two connectors crossing at one point.
- Use separate marker IDs for each connector color. Do not share a neutral marker across colored connectors.
- Every `marker-end="url(#...)"` reference must resolve to a matching `<marker id="...">` in `<defs>`.
- For vertical connectors, align the start and end `x` positions to the visual center or a deliberate port on the source and target edges. Do not leave lines that look offset by a few pixels from their box.
- For horizontal connectors, align the start and end `y` positions to the visual center or a deliberate port on the source and target edges.
- When one node fans out to multiple sibling targets, distribute branches evenly across the target set. Avoid one branch looking straight while others are cramped or sharply bent without a reason.
- Prefer a shared trunk plus evenly spaced branch turns for 3+ sibling targets instead of many unrelated zig-zags.

## Label and Text Placement

Most rendering defects are text that overflows its background, collides with a neighbor, or hides behind a box. SVG does not clip or wrap text automatically, so prevent these by construction:

- **Estimate text width before sizing any pill or box.** Approximate glyph advance per character: monospace ≈ `0.60 × font-size`, proportional sans ≈ `0.55 × font-size`. So `label-width ≈ chars × per-glyph × font-size`. A background pill must be at least `text-width + 16` (8px padding each side). Never emit a pill or box narrower than the text it contains.
- **A label must not overlap any node rectangle.** Compute the label's bounding box from its anchor, estimated width, and font size, then test it against every box in the bounds registry. If it intersects one, move or shorten the label — never let a box paint over label text. This is the most common failure; check it explicitly.
- **Gutters must be wide enough for their labels.** A label dropped into the gap between two boxes needs `gap ≥ label-width + 16`. If the gap is narrower, offset the label just above or below the connector into open canvas, or shorten the text. A connector label sits *beside* the line in clear space, not jammed into a tight crossing.
- **Region titles own a reserved strip.** A region's top-left title occupies a horizontal band along the region's top edge. Keep nodes, chips, and other labels out of that band, and keep the title short enough to clear any box to its right (long region titles silently slide under adjacent boxes).
- **Keep a node's own text inside the node.** If the longest line does not fit the box width, widen the box, lower the font size, or wrap to a second line — never let a line spill past the border.
- **Put prose in the notes rail, not on the canvas.** On-diagram labels are short, fixed phrases; long explanations and caveats belong in the notes rail.

## Editing Priorities

When a generated diagram needs correction, fix issues in this order:

1. Wrong story or missing system element.
2. Arrow direction or endpoint incorrect.
3. Label overlap, clipping, or hidden text.
4. Uneven spacing, unbalanced lanes, or fan-out disorder.
5. Cosmetic polish such as exact centering, rhythm, and visual density.

## Output Modes

### `html-first` Default

Generate only the standalone HTML/SVG artifact. Include toolbar actions for SVG download, PNG download, PNG copy, and print/PDF.

### `html + drawio xml`

Experimental and opt-in. Use only when the user asks for draw.io, Confluence draw.io, editable XML, or a dual artifact. Keep HTML/SVG as the visual source and embed a copyable draw.io XML panel as a secondary export. Validate generated XML by importing it into draw.io before claiming compatibility.

### `drawio-first`

Planned, not yet a stable renderer. Do not advertise `drawio-first` as production-ready until the package includes dedicated mxGraphModel rules, a template, and an import smoke test.

## Notes Rail

Default sections:

- System Shape: runtime boundaries, ownership model, and major component groups.
- Critical Flows: request, auth, data, event, and external dependency paths.
- Operational Notes: scaling, resilience, monitoring, failure domains, and assumptions.

Optional replacement sections:

- Implementation Trace
- Assumptions
- Data Ownership
- Trust Decisions
- Deployment Notes
- Runtime Snapshot, only when the user explicitly asks for current operational state.

## Reliability Guarantees

Every generated artifact must pass a deterministic validation gate before it is returned. The gate has three layers; a failure at any layer blocks delivery until resolved.

### Layer 1 — Input Normalization (before rendering)

- If the brief is ambiguous about the lens, default to `system` and state the assumption in the notes rail.
- If a required entity (actor, entry, state, or external dependency) is missing from the brief, mark it as an assumption rather than inventing details.
- If the input is a diagram-ir JSON, validate that `nodes` and `edges` are non-empty arrays before rendering.

### Layer 2 — Machine Validation (after rendering)

Run `node scripts/check-diagram.mjs <output.html>` and treat any error (exit code 1) as a blocking defect. The checker enforces:

- No template placeholder text remains (E010).
- IR `mode` is `create` or `revise`; IR `lens` is one of the seven supported lenses.
- All IR node and region bounds are inside the viewBox (E005).
- No two IR nodes overlap (E006).
- Every edge references known source and target nodes (E007).
- `data-node-id` / `data-edge-id` attributes match the IR registry bidirectionally (E008).
- Every `marker-end` URL resolves to a defined `<marker>` with matching fill color (E009).
- Connector endpoints land on node edges; no connector segment passes through or hugs any node (E014).
- The artifact is self-contained — no external or relative asset references (E012).

If the checker reports warnings (exit code 0 with W-codes), review them but they do not block delivery. The most common warning is W001 (no IR slot — legacy mode), which means geometry checks were skipped; re-emit the artifact with an embedded IR slot to restore full validation.

### Layer 3 — Visual Verification (final gate)

Render the complete HTML to a raster image (headless Chrome/Chromium, Playwright, or OS preview) and inspect it. Coordinate review alone misses overlaps, clipping, and arrows that fall short. If no renderer is available, fall back to coordinate inspection against the bounds registry and explicitly note the skip.

### Failure Recovery

When the checker fails, fix issues in this order:

1. Placeholder text (E010) — replace with concrete content.
2. Bounds and overlap errors (E005, E006) — adjust coordinates.
3. Connector geometry errors (E014) — re-route connectors.
4. Marker or self-containment errors (E009, E012) — fix references.
5. Structural mismatches (E007, E008) — reconcile IR and SVG.

Re-run the checker after each fix. Only return the artifact when the checker exits 0.

## Release Check

Before final output, run `node scripts/check-diagram.mjs <output.html>`. The checker covers the items marked **[machine]** below (placeholder text, marker integrity, IR geometry, data-attribute cross-checks, region bounds, connector endpoints, connector routing around nodes, self-containment). Items marked **[manual]** need eyes or judgment — the checker cannot see rendered output. If the checker is unavailable, manually verify both groups:

- **[manual] Render the diagram to a raster image and look at it** — coordinate review alone misses overlaps, clipping, and arrows that fall short. Re-render after every fix until the picture is clean.
- **[manual]** No label overflows its pill or its node, and no box paints over a label or region title. If edges carry `labelAnchor` geometry, overlap with node boxes is **[machine]**; everything else is visual.
- **[machine]** No arrowhead ends in empty canvas; every connector touches its target node's edge.
- **[machine]** No connector segment passes through or hugs any node rectangle (source and target nodes excluded); connectors must keep at least 3px clearance from every other node border.
- **[machine]** No connector segment runs collinearly along a node's edge (including its own source or target). A segment may touch a node edge only at its endpoint and only when perpendicular to that edge; any collinear segment that overlaps or merely touches an edge (e.g. exiting a node at a corner and continuing along the border line) is rejected because it visually extends the node stroke.
- **[machine]** No connector segment runs collinearly along a region border for more than a short stub; perpendicular crossings of region borders are allowed.
- **[manual]** Control/policy/dependency edges follow the real direction of dependence, not parallel fans.
- **[machine]** No placeholder text remains.
- **[manual]** The selected lens matches the user's request.
- **[manual]** All visible text uses one language.
- **[manual]** Every visible component maps to the brief or a clearly marked assumption.
- **[manual]** The main path is easy to follow without reading the notes first.
- **[manual]** Stage regions do not hide or collide with components.
- **[machine]** Connectors terminate at component edges.
- **[machine]** Connector arrowheads match connector stroke colors.
- **[manual]** Connector labels do not cover component labels.
- **[manual]** Data persistence and async movement are visible when relevant.
- **[manual]** Trust or policy boundaries are visually distinct when relevant.
- **[manual]** The map key fits inside the viewBox and sits fully inside the 56px reserve band below the lowest component.
- **[manual]** The notes rail is concise and not a second diagram.
- **[machine]** Export buttons reference the generated SVG ID (warning-level).
- **[machine]** The document opens without a build step, network access, or external assets.
- **[machine]** Every `marker-end` URL reference resolves to a matching `<marker>` definition in `<defs>`.
- **[manual]** Vertical gutters between adjacent rows or stacked regions are intentionally consistent, unless they encode a deliberate boundary.
