# Workflow-Aligned Orchestration

Skill2Team must not design an agent team orchestration that drifts away from the original skill or workflow. The original workflow is treated as the baseline operating system.

Workflow preservation means preserving stage order, stage-internal deliverables, required user input nodes, human intervention points, gates, checkpoints, and terminal boundaries unless a rewrite is explicit and reviewed.

Design/package conformance means those preserved workflow requirements are also carried into package artifacts and generated runtime instructions. A workflow map that records a source requirement is incomplete unless the package records how generated agents must enforce it.

## Extract before redesign

| Item | What to capture |
|---|---|
| Trigger | When the original skill starts |
| Inputs | What the user or upstream system provides |
| Stages | The actual ordered steps |
| Stage-internal deliverables | Named artifacts, candidate sets, prompt packages, registries, matrices, files, audit records, checkpoints, and closing handoff prompts produced before a stage hands off |
| Branches | Decision points and alternative paths |
| Loops | Repeated data collection, analysis, revision, or review |
| Gates | Existing checks, validations, approvals, or warnings |
| Required user input nodes | Source settings, choices, approvals, no-auto-continue waits, and terminal/new-request decisions that must pause or ask |
| Human intervention points | User selections, confirmations, explicit no-auto-continue waits, approval prompts, and terminal/new-request boundaries |
| Tools and sources | Tools, scripts, files, APIs, databases, or web sources used |
| Artifacts | Intermediate and final outputs |
| Startup settings | Settings, user choices, runtime conditions, local resources, credentials, or source-required decisions needed before the first real migrated stage |
| Runtime constraints | Required counts, schemas, route/tool restrictions, stage deliverables, gates, waits, checkpoints, terminal rules, and review duties that must be visible in generated agent instructions |
| Known good behavior | Parts users trust or value |
| Failure modes | Parts that cause wrong data, poor quality, delays, or confusion |

## Workflow migration map actions

| Action | Meaning |
|---|---|
| keep | Preserve the step mostly as-is |
| split | Divide an overloaded step among multiple agents |
| merge | Combine low-risk adjacent steps |
| gate | Add independent validation or approval |
| loop | Add a repeated work request and rerun cycle |
| rewrite | Redesign because the original step is unreliable |
| retire | Remove because it is redundant or unsafe |

## Human intervention retention

At the beginning of conversion, ask whether to preserve the source workflow's human-interaction steps, selectively preserve/convert them, or fully automate with audit. Default to `preserve_source_human_interaction_steps`.

Before finalizing the target team, present a concise retention matrix for each human intervention point:

| Choice | Meaning |
|---|---|
| preserve_as_human_wait | Keep the original human decision or no-auto-continue boundary as a runtime wait edge |
| convert_to_reviewer_gate | Replace user confirmation with an independent reviewer gate when the source allows it |
| auto_advance_with_audit | Continue automatically only after logging why automation is safe |
| remove_as_redundant | Remove only when the source step is provably redundant or obsolete |

Default to `preserve_as_human_wait` for source-mandated user input nodes, waits, approvals, selection points, and terminal boundaries. Do not silently auto-advance across them.

Before entering the migrated workflow's first real stage, the entry agent must collect any source-required startup settings and unresolved human-intervention choices. If a required setting is missing and the source does not provide a safe default, the workflow must block rather than silently choosing.

## Runtime constraint materialization

Extract `source_derived_runtime_constraints` from workflow nodes, edges, deliverables, required user input nodes, human waits, gates, checkpoints, schemas, required counts, route/tool restrictions, local-resource dependencies, and review policies.

Each constraint must have an owner or be marked shared. The package must materialize it in `workflow-orchestration.map.json`, `flow-control.contract.json`, `design-package-conformance.contract.json`, `agent-profiles.json`, generated `.codex/agents/*.toml`, and `runtime-instruction-conformance.json`.

If a constraint is missing from downstream package artifacts, set `reexecution_required=true`, name `reexecute_from`, and rerun the earliest responsible phase. Do not repair by editing only runtime instructions.

## Rule

The recommended orchestration must include a short explanation of how each major original workflow stage maps to agents and handoffs. It must also preserve each stage's internal deliverables or explicitly record why a deliverable was rewritten or retired. A summary such as `stage A -> stage B -> review` is not a workflow migration map.
