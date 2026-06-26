# graph-task vNext — md-first collaborative protocol

## Purpose
This spec resets `graph-task` from a `graph.json`-canonical workflow into a **structured-markdown collaborative task protocol**.

The goal is not just prettier visualization.
The goal is to create a task substrate that can be shared across:
- OpenClaw / Linux execution agents
- GitHub as durable sync + history
- Obsidian as the primary human inspection and editing surface
- future human ↔ AI and AI ↔ AI collaboration flows

## Why this reset
The earlier direction treated:
- `graph.json` as canonical state
- Markdown as a projection / inspection layer
- Obsidian as primarily read-only visualization

That split is no longer the best fit.

If Obsidian is a real working surface, and if multiple humans/agents may read and write the same task data, then:
- duplicated canonical layers create avoidable sync risk
- JSON is not the best shared collaboration surface
- git-friendly, append-friendly, human-readable files become more important than a single machine-shaped document

## New canonical rule
**Canonical state lives in markdown files.**

JSON is demoted to support roles only:
- schema references
- validation fixtures
- parser test vectors
- optional export/import or snapshot formats
- internal plugin/runtime derived state if useful

Do not treat JSON as the durable source of truth in vNext.

## Core design goal
Enable deterministic task handling without requiring a monolithic machine-owned state file.

When the markdown tree lives inside a Git-backed vault, treat that repo as the shared canonical workset.
Local edits should be synchronized back into the remote workset rather than allowed to drift as a separate local-only truth.

Determinism should come from:
- strict folder and file conventions
- YAML frontmatter contracts
- explicit append-only / history-preserving rules
- limited write semantics
- git-visible diffs
- protocol-aware tooling and plugin affordances

Not from hiding everything inside one JSON blob.

## Primary worldview
`graph-task` is no longer best understood as a generic graph visualizer.

It is better understood as:
- a **structured task tree protocol** with explicit semantics
- where graph relationships may still exist,
- but tree / containment / execution progression are the first-class interaction model

So:
- tree is primary
- graph is secondary
- deterministic workflow UI matters more than freeform graph rendering

## High-level hierarchy
The conceptual model remains:
- Project
- Step
- Phase
- Node

But the persistent representation becomes a filesystem protocol.

## Canonical filesystem layout
A project run is stored as a folder tree.

Example:

```text
<project-id>/
  index.md
  project-log.md
  steps/
    <step-id>/
      index.md
      step-log.md
      phases/
        <phase-id>/
          index.md
          phase-log.md
          nodes/
            <node-id>.md
            <node-id-2>.md
          results/
            <result-id>.md
            <result-id-2>.md
```

Optional future folders:

```text
<project-id>/
  inbox/
  reviews/
  decisions/
  attachments/
  locks/
```

## Representation rule
- Project / Step / Phase are represented as **folders with `index.md`**.
- Node is represented as a **markdown file**.
- Result history is represented as **append-only result notes** (preferred) or embedded append-only result sections if the simpler model proves sufficient.
- Log / narrative surfaces live in dedicated `*-log.md` files or append-only dated notes.

## Why folder + index.md
Folders express containment.
`index.md` expresses machine-readable metadata + human-readable summary.

This gives:
- intuitive filesystem navigation
- git-friendly diffs
- deterministic discovery
- Obsidian-friendly note handling
- plugin-friendly parsing

## Frontmatter rule
Every canonical entity note must begin with YAML frontmatter.

### Required common fields
Every entity note must include at least:

```yaml
graphTaskVersion: 2
entityType: project|step|phase|node|result
id: <entity-id>
status: pending|active|done|blocked|cancelled
```

### Project `index.md`
Example:

```md
---
graphTaskVersion: 2
entityType: project
id: project-alpha
status: active
title: Project Alpha
goal: Verify md-first collaborative workflow
createdAt: 2026-04-24T13:00:00Z
---
```

Recommended extra fields:
- title
- goal
- description
- createdAt
- updatedAt
- owners
- repo
- tags

### Step `index.md`

```md
---
graphTaskVersion: 2
entityType: step
id: step-1
projectId: project-alpha
stepType: implementation
status: active
createdAt: 2026-04-24T13:10:00Z
---
```

### Phase `index.md`

```md
---
graphTaskVersion: 2
entityType: phase
id: phase-diverge-1
projectId: project-alpha
stepId: step-1
phaseType: diverge
status: active
sequence: 1
createdAt: 2026-04-24T13:20:00Z
---
```

### Node `<node-id>.md`

```md
---
graphTaskVersion: 2
entityType: node
id: node-compare-options
projectId: project-alpha
stepId: step-1
phaseId: phase-diverge-1
nodeType: work
status: active
createdAt: 2026-04-24T13:25:00Z
---
```

### Result `<result-id>.md`

```md
---
graphTaskVersion: 2
entityType: result
id: result-0001
projectId: project-alpha
stepId: step-1
phaseId: phase-diverge-1
nodeId: node-compare-options
status: done
recordedAt: 2026-04-24T14:00:00Z
expected: Compare candidate options honestly
actual: Chose option B after verifying lower complexity
artifacts:
  - references/eval.md
---
```

## Body content rule
Frontmatter is for structured parsing.
Body markdown is for human-readable context.

Recommended sections:
- Summary
- Description
- Current state
- Links / related entities
- Notes
- Decision / rationale
- Next questions

The body may evolve more freely than frontmatter, but frontmatter must remain schema-valid.

## Links rule
Wiki links are for navigation and context, not for canonical discovery.

Meaning:
- the plugin / parser should discover entities from the folder structure + frontmatter
- wiki links are helpful but not the only source of truth

This reduces fragility if links are temporarily missing.

Still, entity notes should include useful links for human navigation.

## Deterministic discovery rule
Canonical entity discovery must work even if note bodies are minimal.

A parser should be able to reconstruct the task tree from:
- folder location
- file name
- frontmatter

without depending on freeform prose.

## Primary semantics
### Project
Top-level unit of work.
Contains Steps.

### Step
Major work partition inside a Project.
Contains Phases.

### Phase
Execution mode unit inside a Step.
Current phase types remain:
- diverge
- converge
- verify
- commit

A Step may repeat:
- diverge
- converge
- verify

A Step should contain at most one commit phase unless a future spec deliberately expands that rule.

### Node
Concrete work item / observation / check / execution unit inside a Phase.

### Result
Expected-vs-actual record attached to a Node.
Results are append-only.

## Append-only bias
This protocol is history-preserving by default.

Preferred operations:
- add a new Step
- add a new Phase
- add a new Node
- append a new Result
- append a new log entry
- mark status forward

Discouraged operations:
- deleting entities
- rewriting history to hide prior states
- mutating older result records
- repurposing old phases to mean something new

If understanding changes, prefer adding a new Phase / Node / Result instead of erasing the old one.

## Sync philosophy
The system is built assuming git-based sync.

This means the persistent shape should optimize for:
- readable diffs
- small conflict surfaces
- append-only updates
- human review of changes
- explicit history

This is one reason md-first is preferred over a single canonical JSON file.

## Concurrency philosophy
If Obsidian becomes a writable working surface, sync semantics matter.

Read-only consumption is easy.
Writeable collaboration is the real design problem.

So vNext must define allowed write patterns early.

## Write-safety rule
Do **not** assume every actor can safely edit every file at any time.

Default design principle:
- many readers
- constrained writers
- append-first mutations

## Conflict minimization strategy
### 1. Split files by entity
Do not keep the whole project state in one document.

### 2. Prefer append-only notes
Appending a new result or log entry is safer than rewriting old content.

### 3. Keep high-contention files small
`index.md` files should hold metadata + concise summary, not giant rolling logs.

### 4. Separate narrative logs from structural metadata
This reduces collisions between state updates and commentary.

## Default write model (recommended)
### Read path
- humans may browse/edit notes in Obsidian
- OpenClaw may read/update via repo checkout
- other agents may read/write through the same protocol

### Safe default write path
- structural mutations happen through protocol-aware tooling or plugin commands
- freeform note edits are allowed in designated log / notes sections
- result creation is append-only
- status changes update frontmatter only in the owning entity note

## Suggested edit permissions by file type
### `index.md` files
High importance.
Should preferably be edited by plugin/tooling rather than casual manual edits.

### `*-log.md` files
Low-risk narrative surface.
Humans and AIs may append more freely.

### `results/*.md`
Append-only creation is preferred.
Existing result files should rarely be edited beyond typo fixes.

### `nodes/*.md`
Moderate risk.
Metadata is structured; body can be richer.

## Locking / ownership options
vNext should not hard-require one locking scheme yet, but should leave room for it.

Candidate models:

### Option A — social protocol only
Rely on git + human discipline.
Best for early experimentation.
Weakest safety.

### Option B — project lease file
A project has a lightweight lock / lease note showing current active editor.
Good for reducing accidental simultaneous structural edits.

### Option C — branch-per-actor
Each actor works on a branch.
Safer, but heavier operationally.

### Option D — entity-level claims
Specific Step or Phase claims rather than project-wide lock.
More scalable, but more complex.

## Recommended near-term concurrency rule
Start simple:
- no hard lock yet
- but treat **structural edits as single-writer at a time per project**
- allow broader multi-reader behavior
- allow append-only logs/results with more flexibility

This is honest and much safer than pretending arbitrary concurrent editing is already solved.

## Obsidian role
Obsidian is not just a passive visualizer anymore.
It becomes a primary human working surface.

But it should not become an unrestricted freeform editor for critical structure.

## Plugin role
The custom Obsidian plugin should become a **protocol-aware deterministic task client**.

Not just a graph renderer.

Its MVP job is to:
- parse the md-first task tree
- render Project / Step / Phase / Node as a structured tree UI
- show statuses, phase types, result counts, and active blockers clearly
- open the underlying notes for human inspection
- provide safe commands for permitted structural operations

## Plugin is preferable because
Our task model is not a generic Obsidian note graph.
It has execution semantics.

What matters most is:
- containment
- execution mode
- status
- result history
- deterministic task navigation

That is better served by a dedicated plugin than by trying to force everything into generic graph view behavior.

## Plugin MVP
Minimum useful plugin behavior:
- detect graph-task projects in the vault
- show tree view:
  - Project
  - Step list
  - Phase list
  - Node list
- show metadata badges:
  - status
  - phase type
  - result count
  - blocked / done state
- open underlying markdown notes on click
- reload / refresh parsed state
- optionally create safe new Step / Phase / Node / Result stubs through controlled commands

## Graph visualization in vNext
Graph visualization is secondary.

Possible later support:
- local subgraph for one Step
- phase transition view
- node dependency mini-map

But the default interaction should be tree-first, not graph-first.

## Validation approach
Because canonical state is markdown, validation should focus on:
- required files exist
- folder containment is valid
- frontmatter schema is valid
- ids match file locations
- cross-references are coherent
- phase rules are respected
- append-only assumptions are not silently violated

## Canonical parser contract
A parser should be able to build an internal model from the md tree and detect:
- Project identity
- Step list and order
- Phase list and order
- Node ownership
- Result ownership
- statuses and timestamps

This derived internal model may be represented as JSON in memory, but that does not make JSON canonical on disk.

## Migration implication
The current Phase 1 / Phase 2 implementation can still be useful as a prototype,
but vNext likely requires a redesign:
- from `graph.json` write-first
- to `index.md` / structured note write-first

So treat earlier JSON-canonical work as learning, not final architecture.

## Immediate next questions
1. Exact folder naming rules: ids only, or numeric sequence prefixes too?
2. Should result history live in separate files by default, or inline until volume proves it painful?
3. What is the smallest safe plugin mutation set for MVP?
4. Do we want a lightweight project lease / lock note in MVP, or only document the single-writer rule first?
5. Which fields are mandatory in frontmatter vs optional in body text?

## Recommended next implementation order
1. freeze md-first filesystem contract
2. freeze frontmatter schema by entity type
3. define validation rules for markdown canonical state
4. define plugin MVP tree UI + safe mutation commands
5. build sample md-first example project
6. build parser + validator
7. build Obsidian plugin MVP
8. only later consider richer graph views or multi-actor lock automation
