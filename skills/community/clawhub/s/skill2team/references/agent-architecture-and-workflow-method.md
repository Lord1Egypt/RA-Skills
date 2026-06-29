# Agent Architecture and Workflow Method

Skill2Team separates agent architecture from workflow orchestration. The separation is mandatory for nontrivial teams.

## Definitions

| Layer | Meaning | Do not confuse with |
|---|---|---|
| Agent Architecture Map | Durable role topology, accountability, authority, context boundaries, skill ownership, and review relationships. | Runtime step order. |
| Workflow Orchestration Map | Runtime control flow: nodes, edges, conditions, loops, gates, fan-out/fan-in, human waits, checkpoints, resume, and terminal boundaries. | Role hierarchy. |
| Control-Flow & Resume Contract | State, artifact lineage, invalidation, rerun, checkpoint, and recovery rules. | A visual architecture diagram. |
| Workflow Preservation Gate | Evidence that source stages, stage-internal deliverables, human intervention points, gates, checkpoints, and terminal boundaries were preserved or intentionally rewritten. | Optional commentary. |

A workflow node may be owned by an existing agent. Do not create a new agent merely because the workflow has a new step.

Keeping a workflow step inside one agent does not make the step's required deliverables optional. Stage-internal artifacts, candidate sets, registries, prompt packages, gates, checkpoints, and handoff prompts still need explicit ownership and stale/reuse rules.

## Architecture patterns

Use these as responsibility patterns:

| Pattern | Use when | Notes |
|---|---|---|
| Coordinator + Specialists | A compact team needs one entry/coordinator, specialist producers, and an independent reviewer. | Default for 5-6 agent teams. |
| Supervisor / Worker | One role routes, manages state, and synthesizes specialist work. | Similar to a parent graph controlling specialist subgraphs. |
| Router + Specialists | Inputs fall into distinct task classes. | Only selected specialists run for each task. |
| Handoff Chain | Ownership moves role to role through explicit contracts. | Good for accountable production flows. |
| Evidence Ledger / Blackboard | Multiple roles share evidence, claims, artifacts, or state. | Requires versioning and gate rules. |
| Reviewer-Gated | Producer or executor output requires independent acceptance. | Required for risk, data, or side effects. |
| Team ReAct Loop | Reason / act / observe crosses agent boundaries. | Otherwise keep ReAct inside one agent. |
| Hybrid Routing | Simple cases stay compact; complex/risky cases activate the full team. | Useful for cost and speed. |

## Workflow primitives

Use these as runtime control-flow primitives:

| Primitive | Required mapping |
|---|---|
| sequence | ordered dependency, owner, input artifact, output artifact |
| embedded stage duty | producer, named deliverable, required shape or count, downstream consumer, stale rule |
| branch / conditional edge | decision owner, condition, chosen path, skipped-path policy |
| loop / retry / repair | trigger, producer, gate, retry budget, stop condition |
| fan-out | item key, per-item inputs/outputs, parallel boundary, partial failure policy |
| fan-in / merge | required inputs, merge owner, conflict policy, downstream artifact |
| gate | acceptance owner, pass/fail criteria, blocked path |
| human wait | required human input, resume condition, no-auto-continue boundary |
| checkpoint / resume | state records, stale detection, restart point, blocked-resume cases |
| terminal | final state, forbidden follow-up actions, new-request boundary |

## Agent count policy

Prefer 5-6 top-level agents for nontrivial teams. Other counts require justification:

| Count | Accept only when |
|---|---|
| 2-4 | Low risk, low data dependency, low iteration, and no independent gate is lost by consolidation. |
| 5-6 | Default target range. |
| 7-8 | Multiple independent gates, hard isolation, separate credentials/workspaces, tool side effects, conflicting professional domains, or parallel specialist groups. |
| >8 | Explicit user requirement for hard isolation or broad regulated domain separation; include a consolidation plan. |

Count top-level accountable roles only. Do not count reusable skills, helper scripts, internal reasoning loops, or workflow nodes as agents.

## Selection sequence

1. Extract source assets and original workflow.
2. Extract stage-internal deliverables and human intervention points before choosing automation.
3. Ask the user which human intervention points should be preserved, converted to reviewer gates, auto-advanced with audit, or removed as redundant.
4. Identify accountability boundaries.
5. Choose an agent architecture pattern and justify the agent count.
6. Build the workflow orchestration map separately.
7. Add control-flow/resume, artifact lineage, and dependency-aware rerun rules.
8. Validate that the architecture map, workflow map, and workflow preservation gate are all necessary, consistent, and not conflated.
