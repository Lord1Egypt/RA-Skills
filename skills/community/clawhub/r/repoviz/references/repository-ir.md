# Repository IR & Evidence Protocol

Read this file when the analysis produces **more than one diagram**, when the user
asks how trustworthy the diagram is, or when wiring architecture diff / reports on
top of an analysis. It defines the lightweight intermediate representation (IR) that
decouples *code analysis* from *URL rendering*, plus the evidence and validation
discipline that makes diagrams verifiable assets instead of AI sketches.

Core principle: **a diagram that renders is not necessarily a diagram that is true.**
Every node and edge should trace back to source code, or carry an explicit
confidence flag.

## The IR Format

One IR document per diagram. Reuse the same node inventory across the suite.

```json
{
  "version": 1,
  "repo": "qiakai/repoviz",
  "commit": "a1b2c3d",
  "scan_mode": "architecture",
  "nodes": [
    {
      "id": "api",
      "label": "API Server",
      "kind": "service",
      "sub": "Express routes",
      "pos": "r0c1",
      "evidence": [
        {"file": "src/api/index.ts", "symbol": "createServer", "lines": "12-40", "level": "verified"}
      ]
    }
  ],
  "edges": [
    {
      "from": "web",
      "to": "api",
      "label": "HTTP",
      "style": "main",
      "evidence": [
        {"file": "src/web/client.ts", "symbol": "fetch", "lines": "8", "level": "inferred"}
      ]
    }
  ],
  "boundaries": [
    {"label": "Edge", "nodes": ["web", "api"]}
  ]
}
```

Field rules:

- `id` — short ASCII slug; stable across the suite (used in URLs, anchors, diffs).
- `kind` — one of: `app service db queue ext person process store source sink
  table view class iface enum actor uc feature milestone`. The Draw adapter maps
  kinds to shapes/colors per diagram type; the IR itself stays renderer-agnostic.
- `evidence` — optional on the object, but a `verified` level is only allowed with
  a real `file` (and `symbol`/`lines` when known). Never fabricate evidence.
- Keep render-only concerns (`t=`, `scheme=`, `w=`, `h=`) **out** of the IR — the
  adapter adds them when encoding the URL.

## Evidence Levels

| Level | Meaning | Bar |
|---|---|---|
| `verified` | Directly seen in source | `file` recorded; open it and the symbol is there |
| `inferred` | Derived from code relationships | naming, config files, import structure, conventions |
| `unknown` | Assumed from common patterns | no code basis yet — must be flagged to the user |

Upgrade/downgrade during validation: an edge left `inferred` must be re-grounded in
code before delivery — either find its `file:symbol` and upgrade to `verified`, or
downgrade to `unknown` and say so. Honest `unknown` beats confident fiction.

## IR → Draw URL Mapping

Map only at encode time; grammar details live in the per-type references.

- **Architecture family** (`archmap`, `arch2`, `uc`, `dataflow`, `erd`, `class`):
  node → `n=id;kind;label[;sub][;pos][;icon]`, edge → `e=from;to[;label][;main|dash]`,
  boundary → `b=label;ids` — see `references/architecture.md`. Note: `b=` id lists
  join with spaces, and **spaces must be `%20`** (raw spaces reset the connection).
- **Sankey** (`?type=sankey`): nodes → `labels=`, edges → `links=From>To:weight`
  (weight from real quantities — file sizes, import counts); see `references/sankey.md`.
- **Sequence / flowchart / lifecycle** (`/draw/seq`, `/draw/mermaid`, `/draw/lifecycle`):
  actors/participants from `person`/`service` nodes, flow from edges; see
  `references/flowchart.md`.
- **Mind map / Gantt** (`/draw/mindmap`, `/draw/gantt`): `feature`/`milestone`
  trees and schedules; see `references/general-charts.md`.
- **Data charts** (`?type=pie|hbar|gauge|combo`): aggregates computed from IR
  quantities (file sizes, module counts), not hand-typed numbers.

## Three-Layer Validation

| Layer | Checks | Tool |
|---|---|---|
| L1 Syntax | URL reachable, renders as SVG/PNG, encoding legal | `bash scripts/validate.sh <url>...` |
| L2 Structure | IR: duplicate ids, dangling edge refs, label collisions, node budget | `bash scripts/validate.sh --ir <file.json>` |
| L3 Fact | Every `inferred`/`unknown` item re-grounded in source, or flagged | Agent re-reads the cited files |

Run L1+L2 before delivering any suite; L3 is part of the analysis loop. On a 4xx
the response body is plain text with a correction example — read it, fix, re-run.

## Quality Report

Append after the diagram suite (default mode, no file writes):

```text
Repository Analysis — <repo> (<scan_mode>, <commit>)
Files inspected: 128 | Modules identified: 12 | Relationships: 34
Evidence: verified 28 · inferred 5 · unknown 1
Validation: L1 pass · L2 pass · L3: 1 unresolved (flagged below)
```

2–5 bullets may follow on the most interesting findings (heaviest coupling, lone
`unknown` nodes, single points of failure).

## Anti-Patterns

- Don't stuff every subsystem into one IR — split at the same boundary you split
  diagrams (15–20 nodes each).
- Don't merge unrelated diagram types into one IR document.
- Don't store render parameters or style choices in the IR.
- Don't emit a quality report with fabricated counts — count what you actually saw.
