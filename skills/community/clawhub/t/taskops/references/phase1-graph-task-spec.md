# Phase 1 — graph-task spec

## Purpose
Phase 1 is the smallest meaningful implementation of the reset direction chosen on 2026-04-23.

Its job is to prove that we can represent work as an explicit graph, update that graph directly, and inspect the state clearly before adding richer visualization or unattended autonomy.

This phase is **not** about full overnight automation.
It is about locking a usable graph-task skill + CLI contract.

## Validation question
Can we define and use a graph-task model that is:
- explicit enough for honest human-readable state
- inspectable enough for human review
- simple enough to use directly from a CLI and OpenClaw skill
- stable enough to become the canonical state layer for later Obsidian and autonomous execution phases

## Out of scope
Do not build these in Phase 1:
- heartbeat-driven autonomous completion loops
- lobster scheduling/execution integration beyond placeholder contracts
- rich graph visualization
- multi-user or multi-tenant concerns
- generalized workflow DSL
- hidden mutation engines or transition engines

## Deliverable
A first usable `graph-task` skill/package with:
- canonical persisted schema
- separately documented high-level structural rules
- a minimal expected-vs-actual result record contract
- a bundled CLI for direct graph editing
- an OpenClaw skill surface
- summary rendering
- independent tests for CLI + skill packaging

## Core references

- `references/schema.graph-task.json`
  - entity structure
  - required vs optional fields
  - containment hierarchy

- `references/rules.graph-task.md`
  - structural rules
  - ownership rules
  - connectivity rules
  - result-record rules
  - current simplifications

- `references/result-record.schema.json`
  - expected-vs-actual writeback record

- `references/cli.graph-task.md`
  - minimal CLI command surface

Supporting references:
- `references/expected-result.schema.json`
- `references/phases.json`
- `references/test-levels.json`

## Current simplifications

1. Use one shared minimal status vocabulary everywhere:
   - `pending`
   - `active`
   - `done`
   - `blocked`
   - `cancelled`
2. Do not introduce a separate mutation layer in this stage.
3. Edit the graph directly through explicit CLI commands.
4. Record expected-vs-actual execution history on `node.results`.
5. If the structure changes, append new Steps / Phases / Nodes / Edges rather than deleting prior history whenever possible.

## High-level hierarchy

`graph-task` currently freezes this hierarchy first:

- `project` = graph of `step`
- `step` = graph of `phase`
- `phase` = rooted graph of `node` and `edge`

Current high-level semantics:
- `step` includes `stepType` and `description`
- `phase` includes `phaseType` and `description`
- `phase.phaseType` uses the functional modes `diverge | converge | verify | commit`
- a step may repeat `diverge`, `converge`, and `verify`
- a step may contain at most one `commit` phase

## Minimal run layout
A usable run should have at least:

- `graph.json`
- `summary.md`

Rules:
- `graph.json` is the canonical state
- `summary.md` is the human-readable inspection surface

## Human inspection surface
Phase 1 must support basic human verification without external visualization.

Minimum inspection outputs:
- current project structure
- step graph summary
- selected step's phase graph summary
- selected phase's rooted node graph summary
- latest expected-vs-actual result records

This can be plain text or markdown.
That is enough for Phase 1.

## Acceptance criteria
Phase 1 high-level contract is complete when all of the following are true:

1. The schema and rules are documented separately.
2. A graph-task project can represent Steps explicitly.
3. Each Step can represent what kind of Step it is via `stepType`.
4. Each Step can store a human-readable `description`.
5. Each Step can contain Phases connected by explicit `phaseEdges`.
6. Each Phase is modeled as a rooted internal node graph.
7. Repeated `diverge`, `converge`, and `verify` Phases can be represented without deleting history.
8. A work node can store expected-vs-actual result records directly.
9. The bundled CLI and skill can be tested independently.

## Recommended next implementation order
1. freeze the high-level schema
2. freeze the high-level rules
3. define the minimal result-record contract
4. implement the CLI surface
5. implement the skill surface
6. smoke-test on at least one happy-path graph flow
