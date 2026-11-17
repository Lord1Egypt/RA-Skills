## Description:

Team Dispatch orchestrates multi-agent workflows with task decomposition, DAG-based parallel execution, durable task tracking, retries, fallbacks, and completion notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vvusu](https://clawhub.ai/user/vvusu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Team Dispatch to split complex requests into specialized subagent work, track task state across context compaction, and collect final deliverables from multi-step workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may change OpenClaw configuration and grant broad subagent delegation.

Mitigation: Review generated OpenClaw configuration before installation and narrow allowAgents to the intended team roster.

Risk: Default setup can create recurring watcher and daily-summary background jobs.

Mitigation: Disable watcher.enabled or dailySummary.enabled, or run setup with --no-watch when recurring jobs are not desired.

Risk: The security verdict is suspicious due to persistent jobs and broad delegation behavior.

Mitigation: Review and scan the skill before deployment, then install only in environments where those behaviors are acceptable.

## Reference(s):

- [Team Dispatch on ClawHub](https://clawhub.ai/vvusu/skills/team-dispatch)
- [Publisher profile](https://clawhub.ai/user/vvusu)
- [CHANGELOG.md](CHANGELOG.md)
- [README.md](README.md)
- [CONFIG.md](references/CONFIG.md)
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with project task JSON, shell commands, configuration changes, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenClaw task files, agent configuration, project files, and watcher or daily-summary jobs when its setup and operational scripts are used.]

## Skill Version(s):

1.0.8 (source: server release evidence and CHANGELOG.md, released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
