# Target-Team Execution Guard Prompt Snippet

Use this snippet inside generated target-team startup prompts and registered entry-agent prompts.

```text
Codex target-team execution guard:
Before performing the task, confirm whether this run is registered target-team execution or current-session target-team fan-out.

Read workflow-preservation-gate.json and workflow-orchestration.map.json before advancing across workflow stages. Preserve source-mandated human waits, approvals, selection points, and terminal boundaries unless the package records an explicit user override. Do not skip stage-internal deliverables such as candidate sets, prompt packages, registries, matrices, audit records, checkpoints, or closing handoff prompts.

For registered target-team execution, confirm that this package is registered in Codex, that the current invocation is the registered entry agent, and that the runtime can hand off to the named specialist agents.

If newly registered target-agent types are unavailable in the active thread but real independent Codex subagents can run, use current-session target-team fan-out instead. Record `target_run_fanout_status=real_session_target_subagents`, keep `registered_target_team_smoke_status=pending_hot_reload_or_new_thread`, and do not claim registered-agent execution.

If neither registered handoff nor real current-session target subagents are available, stop with:

target-team execution blocked
reason: <specific missing runtime capability or evidence>
recovery: <registration, config, or smoke-test step needed>

Do not continue as a single-agent or sequential simulation under the Codex target-team label. API-run role simulation is allowed only when explicitly requested and must be labeled as such.
```
