# TaskOps md-first format

This document defines the canonical markdown-first storage direction for TaskOps.

## Goals

- human-readable and human-editable
- validator-friendly
- append-preserving where possible
- suitable for both skill and Obsidian plugin surfaces
- clear separation between canonical state and derived visualization artifacts
- graph-visible closure through explicit EoW nodes

## Design stance

TaskOps stores **canonical decomposition state** and **canonical execution state** in markdown-first structures.
Derived artifacts such as canvas views, summaries, or exports must stay explicitly non-canonical.

## Top-level work shape

```text
<taskops-work>/
  index.md
  work-log.md
  task-groups/
    <task-group-id>/
      index.md
      versions/
        <version-id>/
          index.md
          decomposition-log.md
          tasks/
            <task-id>.md
          eow/
            <eow-id>.md
  snapshots/
    <snapshot-id>.md
  runs/
    <run-id>/
      index.md
      nodes/
        <run-node-id>.md
        <eow-id>.md
      edges/
        <run-edge-id>.md
      run-log.md
  derived/
    canvases/
    views/
```

Legacy notes:
- old `entityType: project` roots may still be read, but new roots should use `entityType: work`
- old singular `run/` folders may still be read, but new execution graphs should use `runs/<run-id>/`

## Canonical split

### Task graph canonical area
- `task-groups/`
- `snapshots/`
- task-graph EoW nodes under each selected task-group version's `eow/`

### Run graph canonical area
- `runs/<run-id>/`
- run-graph EoW nodes inside the run graph's `nodes/`

### Non-canonical derived area
- `derived/`
- old generated `canvases/` folders when present

## Canonical entity notes

Every canonical entity note should use YAML frontmatter.

Minimum common fields:
- `taskOpsVersion`
- `entityType`
- `id`
- `createdAt`
- `updatedAt?`
- `status?`

## Entity notes

### Work

Path:
- `<work>/index.md`

Suggested fields:
- `taskOpsVersion`
- `entityType: work`
- `id`
- `title`
- `objective`
- `activeRootTaskGroupId`
- `activeSnapshotId?`
- `createdAt`
- `status`

### TaskGroup

Path:
- `task-groups/<task-group-id>/index.md`

Suggested fields:
- `entityType: taskGroup`
- `id`
- `objective`
- `parentTaskId?`
- `activeVersionId?`
- `createdAt`

### TaskGroupVersion

Path:
- `task-groups/<task-group-id>/versions/<version-id>/index.md`

Suggested fields:
- `entityType: taskGroupVersion`
- `id`
- `taskGroupId`
- `version`
- `summary`
- `supersedesVersionId?`
- `selected: true|false`
- `createdAt`

### Task

Path:
- `task-groups/<task-group-id>/versions/<version-id>/tasks/<task-id>.md`

Suggested fields:
- `entityType: task`
- `id`
- `taskGroupId`
- `taskGroupVersionId`
- `title`
- `objective`
- `responsibility`
- `completionCriteria`
- `order`
- `runReadiness?`
- `runReadinessReason?`
- `understandingLevel?`
- `unknowns?`
- `nextLearningGoal?`
- `decompositionConfidence?`
- `executionConfidence?`
- `childTaskGroupId?`
- `runRefs?`
- `createdAt`

Example task↔run reference:

```yaml
runRefs:
  - runId: run-alpha-v1
    runNodeId: run-node-verify
    role: verification
```

Example exploratory task metadata:

```yaml
runReadiness: needs_exploration
runReadinessReason: The task objective is clear, but the API behavior is not understood well enough to decompose.
understandingLevel: partial
unknowns:
  - retry semantics
  - required permission scope
nextLearningGoal: Run a minimal API trial and write the constraints needed for the next decomposition.
```

### EoW for task graph

Path:
- `task-groups/<task-group-id>/versions/<version-id>/eow/<eow-id>.md`

Suggested fields:
- `entityType: eow`
- `id`
- `graphType: task`
- `attachedToType: task`
- `attachedToId`
- `reason`
- `declaredBy`
- `declaredAt`
- `evidenceRefs?`
- `createdAt`
- `status: done`

Example:

```yaml
entityType: eow
id: eow-task-verify-example
graphType: task
attachedToType: task
attachedToId: task-verify-example
reason: no_further_decomposition
declaredBy: ai
declaredAt: 2026-05-08T04:45:00+09:00
evidenceRefs:
  - run:run-alpha-v1/node:run-node-verify
status: done
```

### VersionSnapshot

Path:
- `snapshots/<snapshot-id>.md`

Suggested fields:
- `entityType: versionSnapshot`
- `id`
- `rootTaskGroupId`
- `createdAt`
- `label?`

Body/frontmatter should include a deterministic selected-version map, for example:

```yaml
selectedVersions:
  - taskGroupId: tg-root
    versionId: tgv-root-v1
  - taskGroupId: tg-design
    versionId: tgv-design-v3
```

### Run index

Path:
- `runs/<run-id>/index.md`

Suggested fields:
- `entityType: run`
- `id`
- `workId`
- `createdAt`
- `status`

### RunNode

Path:
- `runs/<run-id>/nodes/<run-node-id>.md`

Suggested fields:
- `entityType: runNode`
- `id`
- `runId`
- `type`
- `title`
- `status`
- `sourceTaskId?`
- `sourceTaskGroupVersionId?`
- `createdAt`

Suggested `type` values include `execute`, `explore`, `debug`, `review`, `verify`, and `delegate`.
Use `explore` when the run objective is learning enough to update task readiness or decomposition.
Use `delegate` when work is intentionally handed to a human, another AI, an agent, or an external system.

Delegation/waiting example:

```yaml
entityType: runNode
id: run-node-human-decision
runId: run-alpha-v1
type: delegate
title: Ask Jimmy to confirm constraints
status: waiting
sourceTaskId: task-user-constraints
sourceTaskGroupVersionId: tgv-root-v1
delegateeType: human
delegateeRef: jimmy
request: Confirm the constraints needed before downstream execution.
expectedOutput: A clear decision and any constraints that update the task graph.
requestedAt: 2026-05-08T04:45:00+09:00
timeoutAt: 2026-05-10T04:45:00+09:00
```

### EoW for run graph

Path:
- `runs/<run-id>/nodes/<eow-id>.md`

Suggested fields:
- `entityType: eow`
- `id`
- `runId`
- `graphType: run`
- `attachedToType: runNode`
- `attachedToId`
- `reason`
- `declaredBy`
- `declaredAt`
- `createdAt`
- `status: done`

Run EoW nodes should usually be connected by a `runEdge` with `edgeType: closes_with`.

### RunEdge

Path:
- `runs/<run-id>/edges/<run-edge-id>.md`

Suggested fields:
- `entityType: runEdge`
- `id`
- `runId`
- `fromRunNodeId`
- `toRunNodeId`
- `edgeType`
- `createdAt`

`fromRunNodeId` and `toRunNodeId` may point to either a `runNode` or an EoW node inside the same run graph.

## Logging files

Append-oriented logs should be plain markdown:
- `work-log.md`
- `decomposition-log.md`
- `run-log.md`

Purpose:
- preserve rationale
- preserve review/audit trail
- avoid hiding important structural changes behind silent rewrites

## Validation targets

Validator should check at least:

### Work
- root `index.md` exists
- new roots use `entityType: work`
- legacy `entityType: project` is readable
- active root task group and active snapshot exist

### Task graph
- required files/folders exist
- ids match paths
- task-group-version ownership is coherent
- sibling task ids are unique within a version
- optional invariant warnings for coverage / orthogonality / closure quality
- only one active version per task group unless explicitly marked otherwise
- active-snapshot terminal task branches have EoW nodes

### Snapshots
- selected task groups exist
- selected versions exist
- selected path is structurally reachable from root

### Run graph
- independent `runs/<run-id>/` folders are valid
- run nodes exist
- run edges reference real run nodes or EoW nodes
- referenced source task/task-group-version ids exist if present
- task `runRefs` and run-node `sourceTaskId` agree bidirectionally
- delegated/waiting nodes include enough request/delegatee metadata
- done terminal run paths have EoW nodes

## Selection model

Important rule:
- version trees may exist broadly
- snapshots materialize chosen paths
- the system should not generate or persist all theoretical combinations

## Derived artifacts

Examples:
- Obsidian canvas exports
- tree summaries
- filtered work views
- visual layouts

All should live under `derived/` or a clearly non-canonical generated surface and be labeled non-canonical.

## Reference example

See `../examples/taskops-canonical-minimal-v1/` for the concrete v1-shaped example using:
- `entityType: work`
- versioned task groups
- a selected snapshot
- explicit EoW nodes
- independent `runs/<run-id>/` graph storage
- bidirectional task↔run references
- a clearly non-canonical derived area

## Migration note

This format is a reset from the earlier `graph-task` md-first project/step/phase/node hierarchy.
That older shape is still useful as source material, but TaskOps v1 should align storage around:
- work roots
- versioned task groups
- explicit snapshots
- explicit EoW closure nodes
- independent run graph separation
