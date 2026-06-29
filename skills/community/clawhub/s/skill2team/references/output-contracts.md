# Output Contracts

Skill2Team produces `design` and `package` outputs. It does not expose delivery modes after `package`, and it does not expose `validate` as a standalone delivery.

## Shared run log

| Field | Meaning |
|---|---|
| route | `source-to-team`, `brief-to-team`, or `guided-to-team`. |
| delivery | `design` or `package`. |
| target_runtime | `codex` when deployable artifacts are requested. |
| architecture_method | framework-neutral agent architecture relationship graph with profile-based agents by default. |
| model_invocation_policy | OpenAI Codex default; direct model API calls only as explicitly labeled API-run role simulation or API-service follow-up. |
| execution_path | `direct-skill` or `meta-team-first`. |
| current_run_fanout_status | `direct-skill-not-requested`, `real_subagents`, `real_session_subagents`, or `blocked_no_real_codex_meta_team`. |

## Design output contract

A design output should include:

1. source asset inventory;
2. current-state diagnosis;
3. original workflow extraction;
4. stage-internal deliverable inventory;
5. required user input node inventory;
6. human intervention inventory and user retention choices;
7. selected human-interaction execution mode, defaulting to `preserve_source_human_interaction_steps`;
8. required startup settings before the first real migrated stage;
9. `source_derived_runtime_constraints`;
10. Agent Architecture Map;
11. Workflow Orchestration Map;
12. Control-Flow & Resume Contract;
13. Workflow Preservation Gate;
14. framework-neutral profile/node/edge notes;
15. agent-count rationale;
16. role cards and independence contracts;
17. skill allocation matrix;
18. handoff and gate contracts;
19. **design quality gate** result;
20. **design/package conformance preflight** result with `reexecution_required` and `reexecute_from` when blocked;
21. local resource allocation map when source material contains bundled local resources;
22. design-continuation prompt templates for package, further design/resource-gate analysis, Codex/OpenAI, API-service runner construction, API-run role simulation, Hermes profile conversion, OpenClaw profile conversion, and other explicitly selected frameworks;
23. unresolved questions and risks.

## Design quality gate

The design quality gate checks:

1. architecture/workflow separation;
2. agent-count rationale;
3. missing or overlapping responsibilities;
4. entry-agent boundary;
5. independent reviewer/gate boundary;
6. missing handoff/state/checkpoint contracts;
7. workflow map has concrete nodes, edges, source-stage mappings, stage-internal deliverables, required user input nodes, gates, checkpoints, and terminal boundaries rather than only a summary;
8. human intervention points were shown to the user for retention choices, with source-mandated user input nodes and waits preserved unless explicitly automated;
9. startup settings required before the first real migrated stage are collected, safely defaulted by source contract, or blocking;
10. source-derived runtime constraints have owners and materialization targets;
11. no task-specific hard-coding in generated names or templates;
12. OpenAI Codex model invocation compliance.

## Package output contract

A package output must include enough information for a recipient to inspect and later use the package without rerunning design.

Required files:

- `design-intermediate-results.json`;
- `docs/design-intermediate-results.md`;
- `agent-architecture.map.json`;
- `docs/agent-architecture-map.md`;
- `workflow-orchestration.map.json`;
- `docs/workflow-orchestration-map.md`;
- `workflow-preservation-gate.json`;
- `docs/workflow-preservation-gate.md`;
- `entry-agent-startup-welcome.json`;
- `docs/entry-agent-startup-welcome.md`;
- `design-output.zip`;
- `design-output-manifest.json`;
- `docs/design-output-archive.md`;
- `design-package-conformance.contract.json`;
- `docs/design-package-conformance-contract.md`;
- `runtime-instruction-conformance.json`;
- `docs/runtime-instruction-conformance.md`;
- `meta-team-audit.contract.json`;
- `docs/meta-team-audit-contract.md`;
- `flow-control.contract.json`;
- `docs/flow-control-contract.md`;
- `local-resource-allocation.map.json`;
- `source-resource-manifest.json`;
- `docs/local-resource-allocation-map.md`;
- `agent-profiles.json`;
- `profiles/*.agent-profile.json`;
- `docs/agent-profiles.md`;
- `.codex/agents/*.toml` for every planned top-level target-team agent;
- `.codex/config.toml`;
- `s2t-agent-registry.json`;
- `.codex/s2t-agent-registrations/<team_id>.json`;
- `runtime-invocation-contract.json`;
- `docs/runtime-invocation-contract.md`;
- `register-readiness-contract.json`;
- `docs/register-readiness-contract.md`;
- `design-continuation-prompt-templates.json`;
- `docs/design-continuation-prompt-templates.md`;
- `post-package-prompt-templates.json`;
- `docs/post-package-prompt-templates.md`;
- `docs/team-usage-guide.md`;
- `AGENTS.md`.

Required manifest fields:

| Field | Meaning |
|---|---|
| team_id | Stable id for this target team. |
| team_kind | `target`, `meta`, or `rehydrated` if a prior capsule is treated as source material. |
| target_runtime | `codex`. |
| architecture_method | framework-neutral agent architecture relationship graph/profile convention by default. |
| model_invocation_policy | OpenAI Codex default, no direct API by default. |
| generated_target_team_agents | List of generated agents and their functions. |
| agent_profiles | Profile ids and paths for generated agents. |
| entry_agent_id | Exactly one user-facing entry agent. |
| registration_status | Must be `not_registered` at package time. |
| entry_agent_runnable | Must be `false` at package time. |
| registered_files | Must be empty at package time. |
| planned_registered_files | Files a later Codex environment may install. |
| package_release_gate | Artifact completeness and readiness checks. |
| design_package_conformance_contract | Design/package conformance status, blockers, and re-execution decision. |
| runtime_instruction_conformance | Per-agent materialization of source-derived constraint ids in runtime instructions. |
| meta_team_audit_contract | Independent meta-team audit requirement and status. |
| design_output_archive | `design-output.zip`, containing design results and design-continuation prompt templates. |
| entry_agent_startup_welcome | Startup welcome page that the generated entry agent must render or summarize before the first migrated workflow stage. |
| next_use_prompt_templates | Package-end Codex package-use prompts only: artifact inspection, package/resource-gate analysis, Codex registration/use after smoke tests, and current-session target-team fan-out. |
| design_continuation_prompt_templates | Design-level prompts for package generation and non-Codex continuations such as API-service runners, Hermes, OpenClaw, or other frameworks. |

## Package release gate

The package release gate checks:

1. all required package files exist;
2. exactly one entry agent is identifiable;
3. all planned top-level agents have Codex TOML and profile artifacts;
4. no hard-coded task-specific package, source, or example identifiers leak into reusable templates;
5. package status remains `not_registered` with no claimed runtime execution proof;
6. workflow-preservation gate passes or blocks package use with explicit missing fields;
7. Workflow Orchestration Map includes concrete `workflow_nodes`, `workflow_edges`, `stage_mappings`, `stage_internal_deliverables`, `user_input_nodes`, `human_intervention_points`, `gate_points`, and `checkpoint_resume_points`;
8. `not_provided_in_plan` is not accepted for source workflow, source inventory, flow control, skill allocation, handoff contracts, or gate/review model in nontrivial source-to-team packages;
9. source-derived runtime constraints are present in design maps, agent profiles, runtime instruction conformance, and generated `.codex/agents/*.toml`;
10. design/package conformance passes or blocks with `reexecution_required=true` and a named `reexecute_from` phase;
11. generated meta-team packages and meta-team-first packages record independent audit status;
12. local resource allocation is present when the source includes bundled local files, and runtime-critical resources are bundled or tied to an accessible `source_root`;
13. entry-agent startup welcome page exists and names required startup inputs plus the default human-interaction preservation policy;
14. `design-output.zip` and `design-output-manifest.json` are present and include the design result;
15. design-continuation prompt templates may include API-service, Hermes, OpenClaw, and other framework paths as design-result material;
16. package-end prompt templates are Codex-only and do not include Hermes, OpenClaw, API-service runner, or framework-construction prompts.

## Final reply prompt rule

Every `design` reply must end with paste-ready continuation prompts for package, further design/resource-gate analysis, Codex/OpenAI registration guidance, API-service runner construction, API-run role simulation, Hermes profile conversion, OpenClaw profile conversion, and other explicitly selected frameworks.

Every `package` reply must end with paste-ready Codex package-use prompts only: artifact-only inspection, package release/resource-gate analysis, Codex registration/use after smoke tests, and current-session target-team fan-out when registered target-agent types are unavailable.

The prompt section must support further analysis by including a resource-gate analysis prompt whenever local resources are present or may have been dropped.

These are follow-up prompts, not additional Skill2Team delivery modes.

## Design-continuation and package-end prompt template contract

`docs/design-continuation-prompt-templates.md` must include the design-level continuation paths, and `docs/post-package-prompt-templates.md` must include package-end Codex package-use prompts only. Together they must include:

1. design-to-package prompt;
2. design-level Codex registration/start guidance prompt using OpenAI Codex model service and placeholders `<SOURCE_SKILL_ZIP>`, `<GENERATED_TARGET_TEAM_PACKAGE>`, and `<CODEX_PROJECT_ROOT>`;
3. design-level API-service runner construction prompt using runtime-specific placeholders only inside design output;
4. registered entry-agent use prompt that is valid only after Codex smoke tests pass;
5. API-runner follow-up prompt labeled as role simulation;
6. Hermes profile conversion prompt using OpenAI Codex model service;
7. Hermes profile conversion prompt using API model service;
8. OpenClaw profile conversion prompt using OpenAI Codex model service;
9. OpenClaw profile conversion prompt using API model service;
10. package-end Codex registration/start prompt;
11. resource-gate analysis prompt that reads `local-resource-allocation.map.json`, `source-resource-manifest.json`, and `docs/local-resource-allocation-map.md`;
12. warning that these are not additional Skill2Team delivery modes;
13. warning that package-end prompts are Codex-only and non-Codex continuations belong in `design-output.zip`.
