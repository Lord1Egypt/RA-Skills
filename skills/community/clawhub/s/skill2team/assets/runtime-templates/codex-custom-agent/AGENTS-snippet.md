# Agent Guidance

Use custom agents for specialized work. Keep delegation shallow unless explicitly requested.

Report the selected execution path and whether real subagent fan-out occurred in the current run. For default `direct-skill`, state `current_run_fanout_status: direct-skill-not-requested`. For Codex `meta-team-first`, use `current_run_fanout_status: real_subagents` only after actual registered meta-agent activation and smoke-test evidence. Use `current_run_fanout_status: real_session_subagents` when real current-session subagents executed fixed S2T work orders while registered custom-agent smoke tests remain pending. If unavailable, block with a reason; do not proceed under the `meta-team-first` label.
