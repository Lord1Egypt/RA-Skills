# Flow Control and Resume

Skill2Team treats nontrivial source-workflow control flow as a first-class migration object. A generated team must preserve control behavior that affects correctness, safety, reuse, checkpointing, or downstream validity.

Workflow preservation depends on explicit stage-internal deliverables, required user input nodes, human intervention points, gates, checkpoint/resume records, and terminal boundaries.

## Control-flow inventory

Capture these elements when present:

| Element | Required mapping |
|---|---|
| sequence | ordered dependency, owner, input artifact, output artifact |
| embedded stage duty | producer, named output, required count or schema, registry/checkpoint update, downstream consumer |
| switch / case | decision owner, inputs, cases, chosen case, skipped-case status, replay requirement |
| branch | branch condition, branch outputs, skipped branch state, downstream trigger rule |
| loop / repair / retry | trigger, producer, reviewer/gate, state owner, retry budget, stop condition |
| back-edge / rerun | rerun source, rerun target, preserved outputs, invalidated outputs, required gates |
| fan-out / parallel group | item key, per-item inputs, per-item outputs, concurrency boundary, partial failure policy |
| fan-in / merge / join | trigger rule, merge owner, required/optional inputs, conflict policy, downstream artifact |
| required user input node | source-required setting, choice, approval, or terminal/new-request input; owner, prompt text, default/block rule, resume target |
| human wait | required human input, resume condition, no-auto-continue boundary |
| human intervention choice | allowed user choices, default preservation action, selected override, audit record when auto-advanced |
| startup setting | required pre-stage input, safe default if any, owner, prompt/block behavior, and downstream invalidation when changed |
| source-derived runtime constraint | stable id, class, owner candidates, package materialization target, and re-execution rule when missing |
| exception / compensation | repair action, redo action, rollback/update rule, escalation owner |
| checkpoint / resume | recoverability records, stale detection, restart point, and blocked-resume cases |
| terminal | final state, forbidden follow-up actions, new-request boundary |

## Agent-internal vs inter-agent control flow

Keep a control-flow fragment inside one agent only when it is local, bounded, does not modify shared state, does not create or overwrite named shared artifacts, does not require an independent gate, cannot make downstream artifacts stale, and has a bounded retry or self-check rule.

Promote a control-flow fragment to inter-agent orchestration when it changes shared state, creates/overwrites/invalidates named artifacts, decides which public stage runs next, requires independent verification or acceptance, depends on user input, uses a restricted route, includes fan-out/fan-in or merge behavior, affects checkpoint/resume safety, or changes a terminal boundary.

## Embedded deliverable preservation

When a source stage contains preparation work before a public handoff, preserve that preparation as workflow structure even if it stays inside one owner agent. Examples include generated candidate sets, prompt packages, registries, indexes, matrices, audit records, checkpoint files, and handoff prompts.

Do not collapse an embedded deliverable into a stage label. The target design must state the producer, required output shape or count, downstream consumer, stale rule, and whether an independent gate reviews it.

## Human intervention policy

Before source conversion starts, ask for the human-interaction execution mode. Allowed top-level modes are `preserve_source_human_interaction_steps`, `selective_human_intervention_retention`, and `fully_automated_with_audit`; the default is `preserve_source_human_interaction_steps`.

During target-team generation, list every detected human intervention point and ask which to preserve. Allowed choices are `preserve_as_human_wait`, `convert_to_reviewer_gate`, `auto_advance_with_audit`, and `remove_as_redundant`.

If the source mandates a wait, selection, approval, or terminal boundary and the user has not selected automation, preserve it as a human-wait edge. Auto-advance must record why the source allows it and what audit record proves the decision.

## Rerun and resume rule

Rerun the smallest affected dependency closure: changed or missing nodes, invalid artifacts, affected merge/gate nodes, and downstream nodes that consumed old inputs. Rerun a whole parallel group only when a shared invariant, schema, policy, environment, or route change makes per-item reuse unsafe.

A checkpoint or resume claim is safe only when the generated team can reconstruct current node statuses, selected cases, loop iterations, parallel item statuses, artifact lineage, gate results, human decisions, and registered runtime artifacts when relevant. If these records are absent, mark the path as `needs_reconstruction` or `blocked` rather than claiming safe continuation.

Design/package conformance failures are rerun events. `design-package-conformance.contract.json` and `runtime-instruction-conformance.json` must record `reexecution_required` and `reexecute_from`. If a required source-derived runtime constraint is absent from design maps, rerun source mapping or workflow orchestration. If it is present in design but absent from agent profiles, manifests, or `.codex/agents/*.toml`, rerun runtime-adapter/package generation. Do not repair by editing only downstream package text.

## Output expectation

For nontrivial workflows, include a flow-control/resume contract in the design or generated package. It should name the owning agent for each decision, loop, gate, merge, parallel group, and terminal boundary, and it should state what becomes stale when upstream outputs change.

The contract is incomplete if it omits `stage_internal_deliverables`, `user_input_nodes`, `source_derived_runtime_constraints`, startup settings, or the human-intervention inventory for a source workflow that contains public user choices, approvals, no-auto-continue prompts, or terminal boundaries.
