# graph-task Obsidian plugin — MVP spec

## Purpose
The plugin is the deterministic Obsidian client for the md-first `graph-task` protocol.

It is **not** primarily a generic graph visualizer.
Its job is to make the canonical markdown task tree:
- discoverable
- inspectable
- safely editable within constrained rules
- usable by humans working alongside AI agents

## Product stance
Primary interaction model:
- tree-first
- protocol-aware
- read-heavy, write-constrained

Secondary interaction model:
- local graph/subgraph views later if they prove useful

Do not optimize the MVP around fancy global graph rendering.
Optimize around reliable task handling.

## Canonical data source
The plugin reads canonical markdown files from the vault.

Discovery depends on:
- folder structure
- `index.md` presence for Project / Step / Phase
- YAML frontmatter

The plugin may build an internal in-memory JSON model for rendering, but markdown remains canonical on disk.

## Detected project layout
A graph-task project root looks like:

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
          results/
            <result-id>.md
```

## MVP user stories
1. As a human, I can open Obsidian and immediately see all graph-task projects in the vault.
2. As a human, I can expand a project into Steps, Phases, Nodes, and Results without manually traversing folders.
3. As a human, I can see status, phase type, and result counts at a glance.
4. As a human, I can click an item and open the canonical markdown note.
5. As a human, I can perform a few safe structural operations from the plugin without hand-editing critical frontmatter.
6. As an AI-assisted operator, I can rely on the plugin to preserve required file structure and frontmatter when creating new entities.

## Core UI surfaces
### 1. Project explorer view
A dedicated side panel showing:
- Project
  - Step
    - Phase
      - Nodes
      - Results

Each row should show compact badges:
- status
- phase type (for phase rows)
- result count (for node or phase rows)
- blocked indicator
- done indicator

### 2. Detail pane / inspector
When an entity is selected, show a structured detail view:
- identity
- status
- ownership fields (`projectId`, `stepId`, `phaseId`, etc.)
- timestamps
- summary fields
- quick links to related canonical notes
- latest results for a node or phase

The detail pane should also include an “Open note” action.

### 3. Validation / refresh controls
The plugin should provide:
- Refresh parsed state
- Re-scan vault for graph-task projects
- Show validation issues for the selected project

## Safe write semantics for MVP
The plugin must not behave like an unrestricted freeform editor for canonical structure.

### Allowed writes in MVP
- Create Project scaffold
- Create Step scaffold under a Project
- Create Phase scaffold under a Step
- Create Node scaffold under a Phase
- Create Result note under a Phase for a Node
- Update status field in frontmatter
- Append timestamped log entries to `project-log.md`, `step-log.md`, or `phase-log.md`

### Disallowed writes in MVP
- Delete Project / Step / Phase / Node from UI
- Rename ids from UI after creation
- Move entities between parents from UI
- Rewrite older result files in bulk
- Auto-merge conflicting concurrent edits
- Freeform frontmatter mutation without validation

### Rationale
These constraints keep the plugin aligned with append-only, history-preserving behavior.

## Concurrency assumptions in MVP
Concurrency is not fully solved yet.

The MVP should assume:
- many readers
- effectively one structural writer per project at a time
- append-friendly logs/results may be less risky than structural edits

The plugin should surface this honestly.

### Optional MVP warning
If a future lightweight project lease file exists, show it.
If not, at minimum show a warning banner like:
- “Structural edits are safest with one active editor per project.”

## Validation rules the plugin should enforce
On load or refresh, detect and surface:
- missing `index.md`
- missing required frontmatter fields
- invalid `entityType`
- mismatched ids vs folder/file names
- Step outside a Project
- Phase outside a Step
- Node outside a Phase
- Result missing a valid `nodeId`
- duplicate sibling ids
- multiple commit phases inside one Step

Validation errors should not silently rewrite files.
They should be shown to the user.

## Suggested row labels
### Project row
- title or id
- status badge
- Step count

### Step row
- id
- step type
- status badge
- Phase count

### Phase row
- id
- phase type badge
- status badge
- Node count
- Result count

### Node row
- title or id
- status badge
- latest result badge if any

### Result row
- result id
- status badge
- recordedAt

## Minimal commands
- `graph-task: Refresh projects`
- `graph-task: Open project explorer`
- `graph-task: Create project`
- `graph-task: Create step`
- `graph-task: Create phase`
- `graph-task: Create node`
- `graph-task: Record result`
- `graph-task: Set status`
- `graph-task: Append project log`
- `graph-task: Append step log`
- `graph-task: Append phase log`

## File-writing behavior
When the plugin creates a new entity, it should:
1. create the correct folder or file path
2. write required YAML frontmatter
3. write a small canonical body template
4. refresh the project explorer

The plugin should prefer creating small, deterministic templates instead of rich prose.

## Body templates
### Project template
Sections:
- Summary
- Goal
- Steps
- Notes

### Step template
Sections:
- Summary
- Description
- Current Phases
- Notes

### Phase template
Sections:
- Summary
- Description
- Nodes
- Notes

### Node template
Sections:
- Summary
- Description
- Work Notes
- Related Results

### Result template
Sections:
- Expected
- Actual
- Notes
- Artifacts

## Out of scope for MVP
- rich graph canvas
- drag-and-drop reparenting
- real-time collaboration protocol
- automatic conflict resolution
- AI orchestration inside the plugin
- advanced diff/review surfaces
- semantic merge engine
- schema migration tooling beyond simple warnings

## Recommended implementation order
1. parser for md-first project structure
2. validation layer
3. project explorer tree UI
4. note opening / detail pane
5. safe scaffold creation commands
6. status update commands
7. log append commands
8. result creation command

## Success criteria
The MVP is successful if:
- a human can browse a project tree faster than by raw file navigation
- the plugin creates valid canonical file structures for the safe commands
- structural edits stay constrained and predictable
- the plugin makes the md-first protocol easier to use without hiding how the files actually work
