# Design/Package Conformance and Re-Execution

Skill2Team must verify that generated target teams preserve source-derived runtime behavior. This check is generic and must not depend on one package name, paper title, task id, or expected figure/workflow shape.

## Conformance chain

For every source-to-team package, track execution-affecting requirements across this chain:

1. source extraction;
2. Agent Architecture Map;
3. Workflow Orchestration Map;
4. Control-Flow & Resume Contract;
5. agent profiles;
6. generated runtime instructions;
7. package manifests and usage contracts.

Execution-affecting requirements include required counts or cardinalities, required schemas, startup settings, stage-internal deliverables, human waits or selections, gates, checkpoints, terminal boundaries, route/tool restrictions, artifact lineage, local-resource dependencies, and independent review duties.

## Source-derived runtime constraints

During design, extract a `source_derived_runtime_constraints` inventory from the source workflow, explicit requirements, stage-internal deliverables, human intervention points, gates, checkpoints, workflow nodes, workflow edges, local resources, and review policies.

Every constraint must have:

- a stable constraint id;
- source field or source reference;
- constraint class;
- concise summary;
- owner candidates when known;
- materialization requirement;
- re-execution rule when missing.

When owner candidates are absent, treat the constraint as shared. Shared constraints must still be visible to generated runtime agents through the package contract or their own instructions.

## Required materialization

The package must materialize source-derived runtime constraints in:

- `workflow-orchestration.map.json`;
- `flow-control.contract.json`;
- `design-intermediate-results.json`;
- `agent-profiles.json` and `profiles/*.agent-profile.json`;
- `.codex/agents/*.toml`;
- `design-package-conformance.contract.json`;
- `runtime-instruction-conformance.json`;
- `docs/team-usage-guide.md`;
- `AGENTS.md`.

If a source constraint affects startup or human choice before a stage starts, the entry agent must ask for it or block. It may use a default only when the source contract names a safe default.

## Conformance result

`design-package-conformance.contract.json` must record:

- `conformance_status`;
- `conformance_blockers`;
- `reexecution_required`;
- `reexecute_from`;
- checked design inputs;
- checked package outputs;
- genericity rule.

`runtime-instruction-conformance.json` must record per-agent materialization of constraint ids in runtime instructions.

## Re-execution rule

When conformance fails, do not repair by editing only downstream package text. Re-execute the earliest responsible phase:

- missing or weak source workflow extraction: rerun source mapping;
- missing stage-internal deliverables, human choices, gates, checkpoints, or constraints in workflow maps: rerun workflow orchestration;
- missing role ownership or profile duties: rerun architecture/profile design;
- missing runtime instruction or manifest materialization: rerun runtime adapter/package generation;
- independent audit failure: route back to the producing meta role and rerun from the earliest failed phase.

The package may be inspected while blocked, but Skill2Team must not claim the target team is source-faithful or runtime-ready.

## Independent meta-team audit

Generated meta-team artifacts and meta-team-first target packages require an independent audit boundary. The reviewer must not be the producer of the artifact under review.

The audit can be performed by registered `s2t-meta-evaluation-reviewer` when available. If the current Codex thread cannot hot-load registered custom agents, a real independent current-session reviewer subagent may perform the same fixed work order and the run must record that status. Role-play by the producing agent is not an audit.

The audit must review:

- source extraction completeness;
- design/package conformance;
- runtime instruction materialization;
- human intervention retention choices;
- local-resource allocation;
- generated meta-team package integrity when the fixed meta-team package is generated or reused.

If the audit blocks, set `reexecution_required=true`, name the responsible producing phase, and rerun that phase before package handoff.
