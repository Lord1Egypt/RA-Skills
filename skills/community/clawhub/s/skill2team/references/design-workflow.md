# Design Workflow

Design is the primary Skill2Team output. It creates a reusable team design before any concrete package is generated.

Workflow preservation is a required part of design for nontrivial source workflows.

## Required design steps

1. Confirm route, delivery, execution path, target runtime, and model invocation policy.
2. Ask for the human-interaction execution mode before source conversion starts: preserve source human-interaction steps, selectively preserve/convert them, or fully automate with audit. Default to preserving source human-interaction steps.
3. Inventory source assets: skills, agents, prompts, tools, scripts, docs, workflows, outputs, and local resources.
4. Diagnose overlap, hidden coupling, missing ownership, prompt reuse issues, and runtime risks.
5. Extract the original workflow without converting every step into an agent.
6. Extract stage-internal deliverables: named artifacts, candidate sets, prompt packages, registries, matrices, files, audit records, checkpoints, and closing handoff prompts produced inside each stage.
7. Inventory required user input nodes: source settings, selections, approvals, no-auto-continue waits, and terminal/new-request choices.
8. Inventory human intervention points: approvals, explicit no-auto-continue waits, selection prompts, review gates, acceptance decisions, and terminal/new-request boundaries.
9. Ask the user which human intervention points to preserve, convert to reviewer gates, auto-advance with audit, or remove as redundant. Default to preserving source-mandated user input nodes, human waits, and choices.
10. Inventory startup settings required before the migrated workflow's first real stage: route, delivery, target runtime, model policy, source material, source-required user choices, credentials, environment settings, local-resource availability, and unresolved human-intervention retention choices.
11. Extract `source_derived_runtime_constraints`: required counts, schemas, startup settings, user input nodes, human waits, gates, checkpoints, stage-internal deliverables, terminal boundaries, route/tool restrictions, local-resource dependencies, and independent review duties.
12. Create the Agent Architecture Map.
13. Create the Workflow Orchestration Map with machine-readable nodes, edges, stage mappings, stage-internal deliverables, required user input nodes, human intervention points, gates, checkpoints, terminal boundaries, and source-derived runtime constraints.
14. Create the Control-Flow & Resume Contract.
15. Define profile-based agents and role boundaries.
16. Map source skills/tools/prompts to accountable agents.
17. Run the design quality gate.
18. Run the design/package conformance preflight: verify each source-derived runtime constraint has a design owner and package materialization target for `design-package-conformance.contract.json` and `runtime-instruction-conformance.json`.
19. If conformance preflight blocks, set `reexecution_required=true`, name `reexecute_from`, and rerun the earliest responsible source-mapping, workflow-orchestration, or architecture/profile phase.
20. Provide design-continuation prompt templates for package, Codex, API-service runners, Hermes, OpenClaw, and other selected frameworks.

## Design quality gate

The design quality gate checks:

- architecture/workflow separation;
- 5-6 top-level agent target or strong rationale;
- exactly one clear entry role;
- independent review where quality risk exists;
- original workflow is represented by concrete nodes, edges, stage mappings, and handoff rules rather than only a prose summary;
- stage-internal deliverables are preserved or explicitly rewritten with rationale;
- required user input nodes are preserved as entry-agent questions or human-wait edges unless the user explicitly chose safe automation;
- human intervention choices are recorded, with source-mandated waits preserved unless the user explicitly chose safe automation;
- startup settings required before the first real migrated stage are either collected, safely defaulted by source contract, or marked blocking;
- source-derived runtime constraints are inventoried and assigned to design/package materialization targets;
- design/package conformance passes or blocks with `reexecution_required=true` and a named `reexecute_from` phase;
- no task-specific hard-coding;
- explicit state, artifact, and context ownership.
