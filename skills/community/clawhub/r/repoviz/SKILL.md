---
name: repoviz
description: >
  Scan any codebase or logic and instantly generate rich visual diagrams—including
  architecture diagrams, flowcharts, Sankey diagrams, sequence diagrams, and mind maps—via
  zero-dependency cloud rendering URLs. Outputs ready-to-embed Markdown links by default,
  with on-demand export to local SVG, PNG, or standalone interactive HTML reports.
  Use when the user asks to visualize a repo, map architecture, trace data flows,
  draw a flowchart/Sankey/sequence diagram, or document system design.
permissions: >
  Network: fetches rendered diagrams from x-cmd.com via explicit, agent-built URLs
  (render, validate, or explicit export only). Exception: the optional short-link
  step (scripts/shorten.sh, explicit user opt-in) uploads the chart definition to
  x-cmd.com, which stores it permanently and publicly. Filesystem: writes only when
  the user explicitly asks to save/export. No package downloads, no installs, no
  background processes, no credential access.
---

# repoviz

Turn a codebase into render-ready diagram URLs. Every diagram is a single
`https://x-cmd.com/draw` URL (flat, percent-encoded parameters) that renders SVG in
browsers, GitHub READMEs, and any Markdown viewer. Default mode writes **no local
files**; local export happens only on explicit request via `scripts/`.

Renders ≠ true: every node and edge carries source evidence (verified / inferred /
unknown) — the output is a verifiable asset, not an AI sketch.

## Step 1 — Intent Analysis & Chart Routing

Pick diagram type(s) from intent + repo shape. Read **only** the matching
`references/` file(s) before constructing that diagram.

| User intent | Diagram | Reference |
|---|---|---|
| System overview, folder hierarchy, microservices, tech stack | Architecture map (`/draw/archmap`) | `references/architecture.md` |
| Request lifecycle, function call chains, API handshakes | Sequence diagram (`/draw/seq`) | `references/flowchart.md` |
| Branching logic, algorithms, auth/pipeline stages | Flowchart (`/draw/mermaid`) | `references/flowchart.md` |
| State machines, statuses, retry/rollback | Lifecycle (`/draw/lifecycle`) | `references/flowchart.md` |
| Data pipelines, dependency/bundle weights, traffic routing | Sankey (`?type=sankey`) | `references/sankey.md` |
| Feature trees, module taxonomy | Mind map (`/draw/mindmap`) | `references/general-charts.md` |
| Roadmaps, schedules, release plans | Gantt (`/draw/gantt`) | `references/general-charts.md` |
| Quantitative repo metrics (language split, coverage, growth) | Data charts (`?type=pie|hbar|gauge|combo|...`) | `references/general-charts.md` |
| Broad "visualize this repo" | **Multi-diagram suite**: 1 `archmap` overview + 1 Sankey (data/dependency flow) or `seq` (core request flow) | the two matching references |

Same-grammar siblings of `archmap` (see `references/architecture.md`): `arch2`
(alt skin). Data/behavior modeling: `uc`, `dataflow`, `erd`, `class` — grammars
and live examples in `references/technical-diagrams.md`. Long-tail charts (treemap,
funnel, graph, ...): `/draw/echarts?d=<url-encoded echarts option JSON>`.

**Scan modes** — scope the scan before reading code (user may pick; default from intent):

| Mode | Scope | Typical output |
|---|---|---|
| `quick` | manifests, tree to depth 2, entry points | 1 overview diagram |
| `architecture` | modules, services, dependency graph | `archmap` (+ Sankey by weight) |
| `deep-dive` | call chains, data flow, state machines | `seq` / flowchart / Sankey suite |
| `impact` | `git diff` vs base: changed files and their dependents | change-flow diagram |
| `full` | all of the above | Repository Report (suite + quality report) |

`impact` mode loads `references/architecture-diff.md` (git-diff delta workflow);
`full` mode loads `references/codebase-report.md` (standard report structure);
repeat scans of the same repo may load `references/incremental-scan.md`
(opt-in cache protocol); multi-diagram or evidence-sensitive work loads
`references/repository-ir.md`.

## Step 2 — Token-Disciplined Codebase Scanning

1. Read root manifests first: `package.json`, `go.mod`, `Cargo.toml`,
   `pyproject.toml`, `docker-compose.yml`, plus a directory tree to depth 3 and the
   declared entry points.
2. Never read every source file. Sample entry-point files and route tables; summarize
   components into high-signal nodes and edges.
3. Derive Sankey weights from real quantities where possible: file sizes (`du -sh`),
   import/reference counts, or traffic/cost figures the user supplies.
4. **URL length guardrail**: keep one diagram to ~15–20 nodes (~60 links for Sankey)
   so URLs stay readable and inside CDN limits. For large repos, emit a high-level
   overview diagram + one diagram per subsystem, never a single dense mega-diagram.
5. Detect language and stack from the manifests and scan with that lens: Go →
   packages/interfaces/goroutines; TypeScript → modules/import graph/API routes; Rust
   → crates/traits/features; Python → packages/decorators/entry points.
6. Record evidence as you scan: every node/edge gets `file[:symbol[:lines]]` and a
   level — **verified** (seen in the code), **inferred** (derived from structure), or
   **unknown** (pattern assumption). Never mark verified without opening the file.

## Step 3 — Construct the URL

- Build the lightweight Repository IR first for suites (one shared node inventory,
  one document per diagram); map IR → URL at encode time. Schema and validation
  protocol: `references/repository-ir.md`.
- Every URL you build carries its labels to the renderer — apply the Step 4
  confidentiality rule before constructing, validating, or exporting it.
- Grammar (nodes/edges/boundaries), encoding table, worked examples, and per-type
  limits live in the reference files. Follow them exactly; every example there is
  live-tested.
- Encoding essentials: space `%20`, `+` `%2B`, `&` `%26`, `#` `%23`, `<`/`>` `%3C`/%3E`,
  newline `%0A`; separators `;` `=` `,` `:` `/` `@` stay literal. No Base64.
- Common modifiers: `title=`, `scheme=dark|light`, `t=<style>` (per-type families in
  references — arch2/seq look best with `t=shadcn`; arch2 nodes take an optional 6th
  `icon` field, e.g. `n=api;be;API;ECS;r2c0;aws:ecs`), `w=`/`h=`, `v=N` to pin a cached
  version, `num=all|peak|none` (charts).
- PNG output embeds a GB2312 level-1 CJK subset: rare characters (e.g. `渲`) become
  tofu in PNG. SVG has no such limit — prefer common synonyms for Chinese PNG labels.
- On a 4xx, the response body is plain text with a correction example — read it,
  fix the offending parameter, retry. Never guess twice.

## Step 4 — Output Delivery

**Default mode — no file writes.** Reply with, per diagram:

```markdown
### <Diagram title>
![<title>](<draw-url>)
*[Interactive preview](<draw-url>)* · [Open in editor](<explore-url>)

- <bullet: what the diagram shows — tiers, critical path, heaviest flows>
- <bullet: notable coupling / single points of failure / ownership boundaries>
```

- `<explore-url>` rewrites `/draw?type=X&q` → `/draw/explore?type=X&q` and
  `/draw/<name>?q` → `/draw/explore/<name>?q` — draw's built-in interactive editor;
  link it, don't rebuild it.
- 2–5 tight bullets per diagram. The image is the deliverable; bullets add judgment.
- **Confidentiality**: rendering — and L1 validation, and `export.sh` downloads —
  sends diagram labels (for flowcharts, the entire program text) to the x-cmd.com
  renderer as URL parameters; they can surface in server access logs (percent-encoding
  is not encryption), and Markdown image embeds may be auto-fetched by clients or
  proxies. Local export does **not** avoid this — the render is still requested from
  x-cmd.com. For confidential repos, warn the user and get explicit approval before
  rendering, validating, or exporting — or render fully offline via a locally
  installed draw CLI.

Close a suite with the quality report (real counts only — never fabricate):

```text
Repository Analysis — <repo> (<scan_mode>, <commit>)
Files inspected: N | Modules: N | Relationships: N
Evidence: verified N · inferred N · unknown N
Validation: L1 pass|skipped (privacy) · L2 pass · L3: N unresolved (flagged below)
```

L1 is **not** automatic — it fetches the URL, i.e. it sends the diagram to
x-cmd.com. For confidential repos run it only with the user's explicit approval
(Step 4 confidentiality rule); otherwise report `L1 skipped (privacy)`. Flag
every `unknown` under its diagram. For explicit "validate" requests or
pre-export checks: `bash scripts/validate.sh <urls...>` (L1 render) and `bash
scripts/validate.sh --ir <ir.json>` (L2 structure). L3 is your re-read of cited files.

**Export mode — only when the user explicitly says** "save locally", "download
SVG/PNG", "export image", "short link", "put this in my README", or "generate
HTML report":

```sh
bash scripts/export.sh "<draw-url>" "<out.svg|png>"        # single download
bash scripts/export.sh --batch <manifest.tsv>              # many: "<url>\t<out>" per line, # comments
bash scripts/shorten.sh <type> '<d-schema json>' [title]   # permanent /draw/c/<hash> (?type= charts only)
bash scripts/build_html.sh "<title>" "<out.html>" '<json>' # standalone report (+ optional ev evidence)
bash scripts/inject_readme.sh "<README.md>" '<json>'       # insert/update diagrams between repoviz markers
```

- `export.sh` downloads via `curl` (fallback: CLIs already installed locally — it
  never fetches or installs packages); `.png` targets auto-get `&format=png` (add
  `&scale=2|3` for higher resolution; pass `scheme=dark` — PNG defaults to light).
  Batch mode: one `url<TAB>output` per line, `#` comments allowed; exits non-zero
  if any item fails.
- `shorten.sh` POSTs the chart definition (the `?d=` JSON schema) to x-cmd.com —
  rate limit ~30/min/IP. Only the `?type=` family accepts POST; node/edge diagrams
  (`/draw/archmap`, `/draw/seq`, ...) return 405 — keep their full URLs. The
  returned `/draw/c/<hash>` renders with GET and is permanent. Run it only on
  explicit user request: the stored definition is permanent and public to anyone
  holding the link (Step 4 confidentiality rule).
- `build_html.sh` takes a JSON array of `{"title","url","note"[,"ev"]}` objects
  (`url` restricted to `https://x-cmd.com` / `https://www.x-cmd.com` draw render
  URLs; `ev` optional, encoded
  `"node|file|symbol|lines|level;..."` — renders a filterable Source-evidence
  table) and emits a self-contained dark/light responsive report: sidebar nav,
  zoom, fullscreen, copy-URL buttons, print-to-PDF friendly. All values are
  HTML-escaped. Example payload:
  `[{"title":"Architecture","url":"https://x-cmd.com/draw/archmap?...","note":"3 tiers; gateway is the single entry","ev":"api|src/api.ts|createServer|12-40|verified"}]`
- `inject_readme.sh` is idempotent: appends a `<!-- repoviz:start -->` …
  `<!-- repoviz:end -->` block (Markdown image + note per diagram) on first use,
  replaces it in place on later runs — diagrams become living assets in the repo.
- After exporting, print the saved path(s) and continue to output the Markdown
  block for the chat so the user gets both.

## Rules

- Brand-neutral: present results as repoviz diagrams; never rename or wrap the
  render URLs.
- One scan, many diagrams: reuse the node inventory across the suite instead of
  re-reading the repo per diagram.
- Prefer fewer, well-chosen nodes over completeness; collapse details into `sub`
  captions and boundary boxes.
- Evidence or it didn't happen: every node/edge is verified, inferred, or flagged
  unknown — never fabricated. Keep the IR/renderer split so suites, reports, and
  future architecture diffs share one inventory; rendering stays a replaceable adapter.
- URL-as-data incremental edits: an existing repoviz diagram is fully defined by
  its URL — **never use vision or image-reading tools** to inspect it. Decode the
  URL from the Markdown, diff its node/edge set against the current code, and emit
  the updated URL in place, preserving node ids, labels, and layout conventions.
