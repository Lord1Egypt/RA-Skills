# Package Workflow

Package is a concrete continuation after design. It produces Codex package artifacts, but it is not the only possible downstream path.

## Required package outputs

- `design-intermediate-results.json` and `docs/design-intermediate-results.md`;
- `agent-architecture.map.json` and `docs/agent-architecture-map.md`;
- `workflow-orchestration.map.json` and `docs/workflow-orchestration-map.md`;
- `workflow-preservation-gate.json` and `docs/workflow-preservation-gate.md`;
- `entry-agent-startup-welcome.json` and `docs/entry-agent-startup-welcome.md`;
- `design-output.zip`, `design-output-manifest.json`, and `docs/design-output-archive.md`;
- `design-package-conformance.contract.json` and `docs/design-package-conformance-contract.md`;
- `runtime-instruction-conformance.json` and `docs/runtime-instruction-conformance.md`;
- `meta-team-audit.contract.json` and `docs/meta-team-audit-contract.md`;
- `flow-control.contract.json` and `docs/flow-control-contract.md`;
- `local-resource-allocation.map.json`, `source-resource-manifest.json`, and `docs/local-resource-allocation-map.md`;
- `agent-profiles.json`, `profiles/*.agent-profile.json`, and `docs/agent-profiles.md`;
- `.codex/agents/*.toml` for each top-level target-team agent;
- exactly one identifiable target entry agent;
- `s2t-agent-registry.json` and `.codex/s2t-agent-registrations/<team_id>.json`;
- `runtime-invocation-contract.json` and `docs/runtime-invocation-contract.md`;
- `register-readiness-contract.json` and `docs/register-readiness-contract.md`;
- `docs/team-usage-guide.md`;
- `design-continuation-prompt-templates.json` and `docs/design-continuation-prompt-templates.md` as design-result artifacts inside `design-output.zip`;
- `post-package-prompt-templates.json` and `docs/post-package-prompt-templates.md`;
- generated target-team agents and functions table.

## Package release gate

The package release gate checks:

- all required artifacts exist;
- generated ids are manifest-derived or placeholder-based;
- no task-specific hard-coding is present;
- profile artifacts align with Codex agent TOML files;
- workflow preservation gate passes, or package use is blocked with concrete missing workflow fields;
- design/package conformance passes, or package use is blocked with `reexecution_required=true` and a named `reexecute_from` phase;
- every `source_derived_runtime_constraints` entry is materialized in design maps, package contracts, agent profiles, generated runtime instructions, usage guidance, and manifests;
- generated runtime instructions tell entry agents to render or summarize `docs/entry-agent-startup-welcome.md`, collect required startup settings, preserve required user input nodes, and resolve human-intervention choices before entering the migrated workflow;
- generated meta-team packages and meta-team-first target packages carry independent audit status in `meta-team-audit.contract.json`;
- workflow-orchestration map has concrete nodes, edges, stage mappings, stage-internal deliverables, required user input nodes, human intervention points, gates, checkpoints, and terminal boundaries rather than only a summary;
- local-resource allocation map is present when source material contains bundled `references/`, `scripts/`, `templates/`, `assets/`, examples, indexes, agents, or release metadata;
- runtime-critical local resources are either bundled in `source-resources/` or the package records a concrete accessible `source_root`; otherwise target execution remains blocked until the resources are restored;
- package-end Codex register/start/use prompts are present and Codex-only;
- target-team execution guard is present in generated agent instructions and usage contracts;
- `registration_status = not_registered`, `entry_agent_runnable = false`, `registered_target_team_smoke_status = not_registered`, `target_run_fanout_status = not_started`, and `registered_files = []` are preserved until a later Codex registration or run step actually runs.

## Target-team execution guard

Every generated Codex target-team package must carry a runtime guard in `docs/runtime-invocation-contract.md`, `docs/team-usage-guide.md`, `s2t-agent-registry.json`, `register-readiness-contract.json`, `AGENTS.md`, and every generated `.codex/agents/*.toml` file.

The generated `.codex/agents/*.toml` files must also carry the design/package conformance guard and all applicable source-derived runtime constraint ids. If `runtime-instruction-conformance.json` reports missing ids, rerun package generation from the runtime adapter instead of editing only TOML text.

The guard must say that registered target-team execution requires real Codex entry-agent invocation and real specialist handoffs. If same-thread hot-load prevents generated target-agent types from being invoked, current-session target-team fan-out is allowed only with real independent Codex subagents and `target_run_fanout_status=real_session_target_subagents`. If neither real path is available, the entry agent must stop with `target-team execution blocked` and must not continue as a single-agent or sequential simulation.

## Required final reply prompts

Every package reply must end with paste-ready Codex package-use prompts only: artifact-only inspection, package release/resource-gate analysis, Codex registration/use after smoke tests, and current-session target-team fan-out when registered agent types are unavailable. These prompts are not new Skill2Team delivery modes.
