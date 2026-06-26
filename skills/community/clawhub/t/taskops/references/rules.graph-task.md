# graph-task high-level rules

This document defines the structural and operating rules for the current high-level graph-task model.
The entity structure itself lives in `references/schema.graph-task.json`.

## Top-level hierarchy

- `project` = graph of `step`
- `step` = graph of `phase`
- `phase` = rooted graph of `node` and `edge`

## Shared status vocabulary

Use the same minimal status set across `project`, `step`, `phase`, `node`, and result records:
- `pending`
- `active`
- `done`
- `blocked`
- `cancelled`

## Operating simplifications for the current stage

1. Do not introduce a separate mutation engine.
2. Edit the graph directly through explicit CLI actions.
3. Preserve history by appending new structure instead of deleting prior structure whenever possible.
4. Record expected-vs-actual execution history on `node.results`.

## project rules

### Role
A project is the top-level work container.
It defines the outer boundary for the whole task graph.

### Rules
1. A project owns its `steps` and `stepEdges`.
2. Every step belongs to exactly one project.
3. `stepEdges` may connect only steps in the same project.
4. A project may start rough or partial; its step graph does not need to be fully connected at initialization.
5. At the project level, only step-level structure is modeled. Node-level or phase-level relations do not bypass step boundaries.

## step rules

### Role
A step is a project-level work unit for one kind of work.
A step answers what kind of work is being done and what that work is about.

### Rules
1. Every step belongs to exactly one project.
2. A step contains zero or more phases while being authored, but a usable step should eventually contain one or more phases.
3. `phaseEdges` may connect only phases in the same step.
4. A step represents one step-level work purpose; its internal phases are functional modes for the same work, not separate higher-level tasks.
5. The order or return path between phases is represented by `phaseEdges`, not by `phaseType` alone.
6. A step may contain multiple `diverge`, `converge`, and `verify` phases.
7. A step may contain at most one `commit` phase.
8. Phase history should be preserved. If a step returns from `verify` to another `diverge`, the earlier phases remain in the graph and the new path is expressed with `phaseEdges`.

## phase rules

### Role
A phase is a bounded step-internal subgraph for one functional mode.
It is the smallest graph unit that must remain internally complete and inspectable.

### Rules
1. Every phase belongs to exactly one step.
2. `phaseType` must be one of: `diverge`, `converge`, `verify`, `commit`.
3. Every phase must have exactly one root node.
4. `rootNodeId` must point to a node inside the same phase.
5. The root node acts as the meta anchor and entry point for the phase.
6. `edges` may connect only nodes in the same phase.
7. Every node in a phase should be reachable from the root node.
8. Phase-to-phase connectivity is not stored inside a phase. The source of truth is the parent step's `phaseEdges`.

## node rules

### Role
A node is the smallest task unit inside a phase.

### Rules
1. Every node belongs to exactly one phase.
2. Node-to-node connectivity is not stored inside node objects. The source of truth is the parent phase's `edges`.
3. Every phase must contain exactly one node with `nodeType = root`.
4. The `id` of that root node must equal the phase's `rootNodeId`.
5. All non-root nodes must use `nodeType = work`.
6. Cross-phase node links are not allowed.
7. A node's meaning is interpreted in the context of its parent `phaseType`:
   - `diverge` => exploration / trial / option work
   - `converge` => synthesis / narrowing / restructuring work
   - `verify` => checking / testing / validation work
   - `commit` => finalization / lock-in work
8. Result records belong on work nodes, not root nodes.

## edge rules

### Role
An edge is a directed connection between two nodes inside a phase.

### Rules
1. Every edge belongs to exactly one phase.
2. `fromNodeId` and `toNodeId` must both reference nodes in the same phase.
3. Edge direction is meaningful and must be preserved.
4. Self-loops are not allowed.
5. Duplicate edges with the same `(phaseId, fromNodeId, toNodeId, edgeType)` are not allowed.
6. The root node must not have incoming edges.
7. Every non-root node should be reachable from the root node.
8. `edgeType = dependency` means the `toNode` depends on the `fromNode`.
9. `edgeType = flow` means the work or reasoning flow proceeds from `fromNode` to `toNode`.
10. Cross-phase node connectivity is not allowed. If higher-level connectivity is needed, express it with `phaseEdges` or `stepEdges` instead.

## result record rules

### Role
A result record is the minimal expected-vs-actual writeback attached to a work node.

### Rules
1. A result record belongs to exactly one node and is stored inside `node.results`.
2. Every result record must keep both `expected` and `actual` text.
3. A result record uses the shared status vocabulary.
4. `artifacts` and `notes` are optional, but should be filled when they materially improve reviewability.
5. Writing a result record is an explicit update to the graph; there is no hidden transition engine behind it.

## phaseEdge rules

### Role
A phaseEdge is a directed connection between two phases in the same step.

### Rules
1. Every phaseEdge belongs to exactly one step.
2. `fromPhaseId` and `toPhaseId` must both reference phases in the same step.
3. `phaseEdge` is the canonical way to represent movement, return, branching, or continuation between phases.
4. Repeated functional loops such as `verify -> diverge` are valid and should be preserved explicitly.

## stepEdge rules

### Role
A stepEdge is a directed connection between two steps in the same project.

### Rules
1. Every stepEdge belongs to exactly one project.
2. `fromStepId` and `toStepId` must both reference steps in the same project.
3. `stepEdge` is the canonical way to express project-level sequencing or dependency between steps.

## Why these rules exist

These rules are meant to keep the model:
- inspectable
- append/refine friendly
- simple enough to use directly from a CLI and skill
- safe for future visualization without changing the top-level graph contract
