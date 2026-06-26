# TaskOps core model

This document freezes the shared conceptual contract for TaskOps.

## 1. Layer split

TaskOps has one top-level container and two connected graph layers.

### 1.1 Work

Purpose:
- hold one objective and its selected decomposition/execution state
- answer whether the work is still open, waiting, or complete

A `work` replaces the old conceptual `project` wording. Legacy `entityType: project` may still be read for compatibility, but new canonical work should use `entityType: work`.

### 1.2 Task graph

Purpose:
- represent decomposition truth
- enforce structural quality
- preserve version history of decomposition changes
- make branch closure explicit with EoW nodes

### 1.3 Run graph

Purpose:
- represent execution truth
- capture real dependency, overlap, reuse, branching, delegation, and waiting
- connect work across levels when reality does not stay tree-shaped

Every run graph is an independent graph under `runs/<run-id>/`. A run graph may reference external tasks or external run nodes, but it should not be merged into another run graph just because it depends on it.

## 2. Main entities

### 2.1 Work

Fields:
- `id`
- `title`
- `objective`
- `activeRootTaskGroupId`
- `activeSnapshotId?`
- `createdAt`
- `status`

### 2.2 TaskGroup

A versioned decomposition unit.

Fields:
- `id`
- `objective`
- `parentTaskId?`
- `activeVersionId?`
- `createdAt`
- `status?`

### 2.3 TaskGroupVersion

A concrete decomposition of one task group.

Fields:
- `id`
- `taskGroupId`
- `version`
- `summary`
- `createdAt`
- `supersedesVersionId?`
- `isSelected`

Contains:
- ordered child tasks
- EoW nodes attached to terminal child tasks
- decomposition rationale
- validation metadata

### 2.4 Task

A child responsibility unit in one specific task-group version.

Fields:
- `id`
- `taskGroupVersionId`
- `title`
- `objective`
- `responsibility`
- `completionCriteria`
- `order`
- `runReadiness?` (`runnable | needs_decomposition | needs_exploration | blocked`)
- `runReadinessReason?`
- `understandingLevel?` (`known | partial | unknown`)
- `unknowns?`
- `nextLearningGoal?`
- `decompositionConfidence?`
- `executionConfidence?`
- `childTaskGroupId?`
- `runRefs?` (`[{ runId, runNodeId, role? }]`)

A task may point to a child task group if it is further decomposed.
If TaskOps does not understand the domain well enough to split a task, the task should be marked `needs_exploration` rather than forcing a fake decomposition.

`runRefs` is the task-side half of bidirectional task↔run traceability. A matching run node should point back with `sourceTaskId` and, when known, `sourceTaskGroupVersionId`.

### 2.5 EoW

EoW means **End of Work** for one graph branch.
It is a first-class node, not just a field, because graph visualization should make terminal branches obvious.

Fields:
- `id`
- `graphType` (`task | run`)
- `attachedToType` (`task | runNode`)
- `attachedToId`
- `reason`
- `declaredBy` (`human | ai | system | agent`)
- `declaredAt`
- `evidenceRefs?`
- `createdAt`
- `status`

Rules:
- A task branch is not structurally closed until a terminal task has an attached task-graph EoW node.
- A run path is not execution-closed until its terminal run node has an attached run-graph EoW node.
- EoW does not mean the whole work is complete by itself; it closes one branch/path.

### 2.6 VersionSnapshot

A selected version path across connected task groups.

Fields:
- `id`
- `rootTaskGroupId`
- `selectedVersionMap`
- `createdAt`
- `label?`

Important:
- a snapshot records a chosen path
- it is not the materialization of all combinatorial version states

### 2.7 Run

An independent execution graph.

Fields:
- `id`
- `workId`
- `createdAt`
- `status`

### 2.8 RunNode

A unit of execution reality.

Fields:
- `id`
- `runId`
- `type`
- `title`
- `objective?`
- `status`
- `sourceTaskId?`
- `sourceTaskGroupVersionId?`
- `createdAt`

Suggested `type` examples:
- `execute`
- `explore`
- `debug`
- `review`
- `verify`
- `delegate`

Delegation/waiting fields for `type: delegate` or `status: waiting`:
- `delegateeType` (`human | ai | agent | system`)
- `delegateeRef`
- `request`
- `expectedOutput`
- `requestedAt`
- `timeoutAt?`
- `onTimeout?` (`escalate | retry | cancel | create_followup`)

A waiting delegated node blocks downstream execution until it is resolved, cancelled, or timed out into a follow-up decision.

### 2.9 RunEdge

A relation between run graph nodes, including EoW terminal nodes.

Fields:
- `id`
- `runId`
- `fromRunNodeId`
- `toRunNodeId`
- `edgeType`
- `note?`

Suggested `edgeType` examples:
- `depends_on`
- `informs`
- `reuses`
- `blocks`
- `follows`
- `tests`
- `waits_for`
- `closes_with`

## 3. Task graph invariants

### 3.1 Coverage

The child tasks in a task-group version must be sufficient to accomplish the parent objective.

Operational test:
> If every child task completes, can we honestly say the parent objective is accomplished?

### 3.2 Responsibility orthogonality

Sibling tasks must not overlap in:
- primary responsibility
- primary ownership of the same deliverable
- completion judgment

Allowed:
- shared context
- mutual influence
- downstream impact on each other
- overlap in actual execution work inside the run graph

Not allowed:
- two sibling tasks both being the primary owner of the same thing
- two sibling tasks requiring the same completion judgment to be considered done

### 3.3 Closure

Each task must have a locally understandable completion boundary, and every terminal selected branch must eventually end with an EoW node.

Operational tests:
> Can a human say what “done” means for this task without reading the entire project history?

> Does every terminal branch in the active snapshot visibly close with EoW?

## 4. Completion rule

A work is complete when:

```text
active snapshot terminal task branches all have task-graph EoW
+ required terminal run paths have run-graph EoW
+ there are no unresolved waiting/delegated/blocking run nodes
```

This makes completion graph-visible instead of implicit.

## 5. Task graph operations

### 5.1 `decompose`

Creates the first concrete child-task set for a task group.

Input:
- parent task group objective
- rationale
- proposed children

Output:
- new `TaskGroupVersion`
- child `Task` records
- optional validation report

### 5.2 `refactor`

Creates a new version of an existing task group.

Use when:
- coverage is weak
- sibling responsibility is overlapping
- completion boundaries are unclear
- learning changed the best decomposition

Important:
- refactor does not erase old decomposition history
- refactor creates a new `TaskGroupVersion`
- child subtrees become version-dependent under the chosen path

## 6. Run graph rules

The run graph may be messier than the task graph. That is expected.

Allowed in run graph:
- overlapping work
- cross-level work relations
- one run node helping multiple tasks
- reused outputs
- exploratory loops
- explicit debugging, verification, and review work
- human/AI/agent delegation and waiting
- references to external run graphs

Exploratory run nodes are valid execution truth when their objective is learning: search, try/error, prototype, debug, or review enough context to improve the next task-graph decision.

The run graph should tell the truth about how work actually unfolded, even when that truth is not tree-shaped.

## 7. Relation between task and run layers

### 7.1 Bidirectional traceability

A task may list `runRefs`.
A run node may link back with `sourceTaskId` and `sourceTaskGroupVersionId`.

Validator behavior:
- task `runRefs` should resolve to real run nodes
- referenced run nodes should point back to the source task
- run nodes with `sourceTaskId` should have matching task-side `runRefs`

### 7.2 Non-isomorphism

The run graph is not required to mirror the task graph one-to-one. That would be a design mistake.

Task graph answers:
> What is the right decomposition?

Run-readiness classification answers:
> Should this task run now, decompose next, explore first, or wait on a blocker?

Run graph answers:
> What actually happened in execution?

### 7.3 Honest divergence

If real work repeatedly violates a decomposition, that is a signal to consider `refactor`.
The solution is not to falsify the run graph.

## 8. Immediate implementation implications

The implementation should favor:
- explicit ids
- visible EoW terminal nodes
- bidirectional task↔run references
- independent `runs/<run-id>/` graphs
- append-preserving history
- version selection over destructive overwrite
- validator checks for task-graph closure and run-graph waiting/delegation
- md-first human inspectability

The implementation should avoid:
- hidden closure fields that do not show up in graph views
- combinatorial snapshot explosion
- implicit mutation magic
- overfitting the model to one UI surface
