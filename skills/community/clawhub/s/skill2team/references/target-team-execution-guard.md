# Target-Team Execution Guard

This guard applies to every generated target-team package when the selected runtime is Codex.

## Hard rule

A generated target team may be described as registered target-team execution only after the package has been registered and runtime evidence confirms the entry agent can hand off to every required specialist agent.

If a same-thread Codex hot-load miss prevents newly registered target-agent types from being invoked, Skill2Team may still run the target team through real current-session Codex subagents when the active session can launch independent subagents for the generated target profiles. That run must be labeled `target_run_fanout_status=real_session_target_subagents` and must keep registered smoke status pending.

Codex target-team execution must never silently degrade into a single-agent or sequential role-play run.

## Entry-agent blocker

The generated entry agent must stop with:

```text
target-team execution blocked
reason: <specific missing runtime capability or evidence>
recovery: <registration, config, or smoke-test step needed>
```

when any of these are true:

- the entry agent was not invoked as a registered Codex custom agent and no real current-session target-team fan-out is being used;
- `.codex/config.toml` does not expose the generated agents through `config_file` entries;
- `multi_agent` or `enable_fanout` is unavailable when required by the package;
- specialist agent handoff cannot be performed in the runtime and real current-session target subagents are unavailable;
- post-registration smoke-test evidence is missing and real current-session target subagent evidence is missing;
- the user is asking for Codex target-team execution but only an API runner or unregistered package inspection is available.

## Forbidden behavior

Under Codex target-team execution, the entry agent must not:

- say it will run the specialist agents as a sequential simulation;
- collapse the generated team into one role;
- perform specialist work itself while claiming specialist handoff;
- label current-session subagent fan-out as registered target-team execution;
- copy source-skill self-invocation prompts as the target-team startup prompt;
- mark `entry_agent_runnable=true` without runtime smoke-test evidence.

## Allowed alternatives

- **Artifact-only inspection** before registration: inspect package files and explain blockers; do not perform the target workflow.
- **Current-session target-team fan-out** when registered target-agent types are unavailable in the active thread: launch real independent Codex subagents for generated target profiles, record `target_run_fanout_status=real_session_target_subagents`, keep `registered_target_team_smoke_status=pending_hot_reload_or_new_thread`, and do not call it registered execution.
- **API-run role simulation** only when the user explicitly chooses API model service. It must be labeled as API-run role simulation and not described as Codex custom-agent execution.
- **API-service follow-up or external framework continuation** only when explicitly selected and labeled outside Codex target-team execution.
