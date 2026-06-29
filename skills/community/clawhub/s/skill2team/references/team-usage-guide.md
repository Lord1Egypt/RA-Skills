# Team Usage Guide Reference

Every generated package must include `docs/team-usage-guide.md`.

## Required sections

1. Package status: `not_registered`, `entry_agent_runnable = false`, `registered_target_team_smoke_status = not_registered`, `target_run_fanout_status = not_started`, `registered_files = []`.
2. Model invocation policy: OpenAI Codex default; direct API calls only as labeled API-run role simulation or API-service follow-up in design-continuation material.
3. Architecture method: framework-neutral agent architecture relationship graph with profile-based agents.
4. Generated target-team agents and functions table.
5. Entry-agent startup welcome page: `entry-agent-startup-welcome.json` and `docs/entry-agent-startup-welcome.md`.
6. Human-interaction preservation mode: default to `preserve_source_human_interaction_steps`; full automation requires explicit user selection and audit records.
7. Agent profiles list and profile file paths.
8. Before-registration usage: artifact-only inspection; target workflow execution requires Codex registration and smoke-test evidence.
9. Design output archive: `design-output.zip` and `design-output-manifest.json`, including design-continuation prompt templates.
10. Package-end Codex registration/start prompt using OpenAI Codex model service.
11. Registered entry-agent prompt valid only after Codex smoke tests pass.
12. Current-session target-team fan-out prompt with `target_run_fanout_status=real_session_target_subagents`.
13. Safety and no-hard-coding notes.

Package-end guidance is Codex-only. API-service runner, Hermes, OpenClaw, or other framework continuations belong in design output and `design-output.zip`, not in package-end prompt templates.

## Required package-end Codex registration/start prompt

```text
Start Skill2Team.
Route: source-to-team
Delivery: package
Execution path: direct-skill
Target runtime: codex
Model invocation policy: use OpenAI Codex; do not call direct model APIs.
Source material: <SOURCE_SKILL_ZIP>
Generated target-team package: <GENERATED_TARGET_TEAM_PACKAGE>
Package-end action requested: provide manifest-scoped instructions to register and start this shared target-team package in Codex.
Read s2t-agent-registry.json, agent-profiles.json, entry-agent-startup-welcome.json, docs/entry-agent-startup-welcome.md, docs/team-usage-guide.md, docs/runtime-invocation-contract.md, docs/register-readiness-contract.md, and docs/post-package-prompt-templates.md.
List the generated target-team agents and their functions.
Use the package's framework-neutral Agent Architecture Map as the conceptual topology, but register only manifest-scoped Codex custom-agent files under <CODEX_PROJECT_ROOT>.
Give manifest-scoped Codex registration steps, smoke tests, and the prompt to invoke the registered entry agent after Codex smoke tests pass.
If the registered entry agent cannot hand off to required specialists because generated target-agent types are unavailable in the active thread, use current-session target-team fan-out only when real independent Codex subagents can run and record `target_run_fanout_status=real_session_target_subagents`; otherwise stop with `target-team execution blocked`.
Do not claim the target team is runnable until Codex entry invocation, specialist handoffs, reviewer gate blocking, startup welcome rendering, and state/artifact handoff have evidence.
```

## Required registered entry-agent use prompt

```text
Use the registered `<ENTRY_AGENT_ID>` agent.
Task: <what you want this team to do>.
Inputs: <files, state path, or pasted context>.
Start by rendering or summarizing docs/entry-agent-startup-welcome.md.
Collect required startup inputs and ask whether to preserve source human-interaction steps, selectively preserve/convert them, or run fully automated with audit. Default to preserving source human-interaction steps.
Use shallow specialist handoffs. If specialist handoff cannot run, stop with `target-team execution blocked`; do not continue as sequential or single-agent simulation.
```

## Required current-session target-team fan-out prompt

```text
Run this generated target-team package through real current-session Codex subagents, not through registered custom-agent execution.
Generated target-team package: <GENERATED_TARGET_TEAM_PACKAGE>.
Read s2t-agent-registry.json, agent-profiles.json, entry-agent-startup-welcome.json, agent-architecture.map.json, workflow-orchestration.map.json, docs/entry-agent-startup-welcome.md, docs/runtime-invocation-contract.md, and docs/team-usage-guide.md.
Use this only when registered target-agent types are unavailable in the active thread but real independent Codex subagents can run.
Spawn real independent subagents for the generated specialist profiles and keep entry, specialist, and reviewer responsibilities separate.
Record target_run_fanout_status=real_session_target_subagents, registered_target_team_smoke_status=pending_hot_reload_or_new_thread, and registered_agent_invocation_verified=false.
Do not claim registered target-team execution and do not continue as sequential or single-agent simulation.
```

## Required registered target-team execution guard

When the package is registered and the entry agent is invoked in Codex, the entry agent must verify real specialist handoff before doing the target workflow. It must also render or summarize the startup welcome page and preserve source-required user input nodes and human waits unless the user explicitly selected safe automation.

If registered handoff is unavailable but real current-session target subagents can run, the workflow may continue only with `target_run_fanout_status=real_session_target_subagents` and registered smoke status pending. If neither real path is available, it must stop with:

```text
target-team execution blocked
reason: <specific missing runtime capability or evidence>
recovery: <registration, config, or smoke-test step needed>
```

It must not continue as a sequential or single-agent simulation under the Codex target-team label.
