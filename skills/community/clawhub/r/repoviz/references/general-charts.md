# Mind Maps, Gantt & Auxiliary Charts

## 1. Mind Map — `/draw/mindmap`

### When to Use

Feature trees, module taxonomies, roadmap breakdowns, decision trees — any single-rooted hierarchy the user wants to explore radially.

### URL Schema & Encoding Rule

```
https://x-cmd.com/draw/mindmap?n=<root>/<branch>/<leaf>[&n=<root>/<branch2>...][&style=organic|tree|radial][&title=]
```

- Each `n=` is one **root-to-leaf path**; shared prefixes merge automatically, so listing the leaves rebuilds the whole tree.
- **Single tree only** — every path must share the same root segment, else 400: `mindmap takes one tree — root "X" differs from "Y"`.
- `style=`: `organic` (bezier curves, default), `tree` (boxed nodes with elbow connectors), `radial` (root-centred fan).
- Space inside a segment → `%20`; segments are split on literal `/`.

### Minimal Working Example

```
https://x-cmd.com/draw/mindmap?n=Product/Features/Speed&n=Product/Features/Offline&n=Product/Markets/EU&title=Minimal%20mindmap
```

### Production Repo Example

Two-sprint roadmap, organic style:

```
https://x-cmd.com/draw/mindmap?style=organic&title=Roadmap&n=Roadmap/Sprint%201/Auth&n=Roadmap/Sprint%201/Cache&n=Roadmap/Sprint%202/API&n=Roadmap/Sprint%202/Export
```

### Anti-Patterns & Limits

- ≤500 nodes, ≤8 levels deep; beyond that, split into per-area mind maps.
- Do not use `/` inside a label (it is the path separator) — rephrase or use `-`.
- `tree` style reads best for formal docs, `radial` for brainstorming walls; pick one style per report.

## 2. Gantt — `/draw/gantt` & `/draw/gantt2`

### When to Use

Project schedules, release plans, migration timelines, milestone tracking.

### URL Schema & Encoding Rule

Mermaid Gantt DSL, whole program in `m=`, `%0A` between lines:

```
https://x-cmd.com/draw/gantt?m=gantt%0A  dateFormat YYYY-MM-DD%0A  section <Name>%0A  <Task> :[status,] [id,] <start|after id>, <duration|end>
```

- `dateFormat YYYY-MM-DD` then tasks: `Design :done, a1, 2026-11-01, 3d` or `Build :a2, after a1, 5d`.
- Status keywords color the bar: `done`, `active`, `crit` (critical).
- `gantt2` renders the same `m=` with an alternate skin — use it when the default look clashes with a report theme.

### Minimal Working Example

```
https://x-cmd.com/draw/gantt?m=gantt%0A%20%20dateFormat%20YYYY-MM-DD%0A%20%20section%20Dev%0A%20%20Design%20%3Adone%2C%20a1%2C%202026-11-01%2C%203d%0A%20%20Build%20%3Aa2%2C%20after%20a1%2C%205d
```

### Production Repo Example

Release plan across two sections with dependency chaining:

```
https://x-cmd.com/draw/gantt2?title=Release%20plan&m=gantt%0A%20%20dateFormat%20YYYY-MM-DD%0A%20%20section%20Core%0A%20%20Scan%20engine%20%3Adone%2C%20s1%2C%202026-11-02%2C%204d%0A%20%20Chart%20router%20%3Aactive%2C%20s2%2C%20after%20s1%2C%203d%0A%20%20section%20Export%0A%20%20HTML%20report%20%3As3%2C%20after%20s2%2C%205d
```

### Anti-Patterns & Limits

- `?` and `:` inside task names break parsing (`:` is the task separator) — keep names plain, `%3A` if truly needed.
- Dateless tasks are not allowed: give an explicit date or `after <id>`.
- Very wide plans (> ~12 tasks) should be split per section/milestone, or widen with `w=` (max 1600).

## 3. Auxiliary Data Charts (repo metrics)

Useful companions when the user asks for quantitative repo health alongside structure diagrams. All are `https://x-cmd.com/draw?type=<type>` with flat parameters; full vocabulary in the routing table of `SKILL.md`.

| Chart | URL pattern | Verified example |
|---|---|---|
| Language share | `type=pie&labels=L1,L2&values=bytes1,bytes2` | `https://x-cmd.com/draw?type=pie&labels=TypeScript,Shell,Python,CSS&values=4821,2312,980,412&title=Language%20bytes` |
| Language ranking | `type=hbar&labels=...&values=...` | `https://x-cmd.com/draw?type=hbar&labels=TypeScript,Shell,Python,CSS&values=4821,2312,980,412&title=Language%20bytes` |
| Test coverage | `type=gauge&value=87&max=100` | `https://x-cmd.com/draw?type=gauge&title=Test%20coverage&value=87&max=100&scheme=dark` |
| Commits + downloads | `type=combo&series=name:v,v&line=name:v,v` | `https://x-cmd.com/draw?type=combo&labels=Q1,Q2,Q3,Q4&series=downloads:120,180,260,340&line=stars:3,5,8,13&title=Growth` |

Limits that matter here: pie ≤100 categories (>9 auto-merge to *Other*), bar/hbar ≤30 groups, line/area ≤60 points, radar 3–12 axes, scatter ≤200 points. `num=all|peak|none` controls value labels; `v=N` pins a cached version.
