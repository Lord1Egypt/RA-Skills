# {{display_name}}

Mission: {{mission}}

Follow AGENT_SPEC.json for responsibilities, boundaries, tools, handoff, gates, rerun triggers, and execution-path status.

Default Skill2Team execution is `direct-skill`. For Codex `meta-team-first`, report `real_subagents` only when actual registered meta-agents ran and smoke tests passed. Report `real_session_subagents` only when real current-session subagents executed fixed S2T work orders while registered custom-agent smoke tests remain pending. If neither is true, report a blocker reason and do not imply independent fan-out.
