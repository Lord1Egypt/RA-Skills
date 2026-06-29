# Runtime Invocation and Prompt Rewrite

Two common failures must be prevented:

1. generated agent artifacts are mistaken for already registered, runnable agents;
2. source-skill self-invocation prompts are copied into target-team prompts.

## Model invocation policy

Skill2Team, the fixed S2T meta-team agents, and generated target-team agents default to OpenAI Codex runtime/custom-agent invocation. Direct API model runs are allowed only when explicitly labeled as API-run role simulation or API-service follow-up.

## Architecture/profile policy

Generated packages use framework-neutral agent relationship architecture by default. Profiles are durable agent nodes; architecture and workflow maps define edges, gates, checkpoints, user input nodes, human waits, and terminal boundaries. A specific runner framework is optional and belongs only to an explicitly selected design-continuation or API-service follow-up.

## Runtime status fields

| Field | Meaning |
|---|---|
| `target_team_registration_status` | `not_registered` at package time. |
| `entry_agent_runnable` | `false` at package time. |
| `registered_files` | Empty at package time. |
| `generated_target_team_agents` | All generated target-team agents and functions. |
| `agent_profiles` | Profile artifacts for every generated target-team agent. |
| `registered_target_team_smoke_status` | `not_registered`, `pending_hot_reload_or_new_thread`, or `passed`. |
| `target_run_fanout_status` | `not_started` or `real_session_target_subagents` for current-session Codex subagent execution. |
| `current_task_execution_mode` | direct-skill, Codex fan-out, blocked Codex meta-team-first, artifact-only, API-run role simulation, or API-service follow-up. |
| `design_package_conformance_status` | `passed` or `blocked` from `design-package-conformance.contract.json`. |
| `runtime_instruction_conformance_status` | `passed` or `blocked` from `runtime-instruction-conformance.json`. |
| `reexecution_required` | `true` when design/package or runtime instruction conformance blocks use. |

## Invocation wording

| State | Allowed wording |
|---|---|
| Package generated but not registered | `Inspect this generated package as artifacts only; do not perform the target-team task or claim Codex registered-agent execution. Register and smoke-test first.` |
| Codex registration and smoke tests passed | `Use the registered <entry_agent_id> agent. If specialist handoff is unavailable, stop with target-team execution blocked.` |
| Same-thread target-agent hot-load miss, real subagents available | `Run current-session target-team fan-out with target_run_fanout_status=real_session_target_subagents; do not claim registered-agent execution.` |
| API runner selected | `Run API-role simulation using the package docs; do not claim Codex custom-agent execution.` |
| API-service runner selected | `Build an API-service follow-up from package profiles; do not claim Codex custom-agent execution.` |
| Hermes uses OpenAI Codex service | `Convert profiles in Hermes and use OpenAI Codex as the model service.` |
| Hermes uses API model service | `Convert profiles in Hermes and label the run API-service follow-up.` |

Do not tell the user to invoke a registered entry agent in the unregistered case.

Before runtime use, read `design-package-conformance.contract.json`, `runtime-instruction-conformance.json`, and `meta-team-audit.contract.json`. If any reports `reexecution_required=true` or blocks runtime claims, rerun the named Skill2Team phase before using the package for source-faithful execution.

## Source prompt rewrite

Source invocation patterns such as `Use <source skill> skill` are source-local. Generated target-team prompts must rewrite them to the target entry-agent contract. This rule is manifest-derived and must not hard-code a specific source example.

Use placeholders in shared templates:

```text
<SOURCE_SKILL_ZIP>
<GENERATED_TARGET_TEAM_PACKAGE>
<CODEX_PROJECT_ROOT>
<HERMES_WORKSPACE>
<API_SERVICE_PROJECT_ROOT>
<MODEL_API_SERVICE_CONFIG>
```

## Codex target-team execution guard

When a generated target team is executed in Codex as registered target-team execution, the entry agent must verify that it is operating as the registered entry agent and that the runtime can hand off to named specialist agents. If the runtime cannot perform the handoff because the active thread did not hot-load generated target-agent types, it may continue only by launching real current-session subagents for the generated target profiles, recording `target_run_fanout_status=real_session_target_subagents`, and keeping registered smoke status pending. If neither registered handoff nor real current-session target subagents are available, the entry agent must stop with `target-team execution blocked`, state the reason, and give recovery steps.

The entry agent must not say it will run the specialists through sequential simulation, single-agent fallback, or role-play while presenting the result as Codex target-team execution. API-run role simulation is allowed only when explicitly selected and labeled as API-run role simulation.
