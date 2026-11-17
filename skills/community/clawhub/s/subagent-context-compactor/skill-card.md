## Description:

Context Compactor monitors and compresses long OpenClaw session context with HOT/WARM/COLD tiers, token and message-count triggers, local storage, and status reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoshan](https://clawhub.ai/user/geoshan)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to reduce token use and preserve important session history during long OpenClaw conversations. It supports manual and automatic compaction, monitoring, and local reports for context-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill persistently monitors the workspace and can read and store sensitive OpenClaw memory and agent-instruction data.

Mitigation: Use it only in approved workspaces, restrict file permissions on generated databases and logs, and define retention, deletion, and access controls before enabling monitoring.

Risk: The artifact includes automatic monitoring, cron examples, and local retention of original context data.

Mitigation: Disable cron jobs and auto-start behavior unless explicitly needed, and periodically purge or rotate stored status, log, and SQLite data.

Risk: The security guidance calls out hard-coded outbound alert examples and plaintext original-context retention as review items.

Mitigation: Remove outbound alert examples and plaintext original-context retention unless they are required and covered by documented operational controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/geoshan/skills/subagent-context-compactor)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Context Management](https://docs.openclaw.ai/context-management)
- [OpenClaw Token Optimization](https://docs.openclaw.ai/token-optimization)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, Python code snippets, and local status or report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite history, JSON status data, logs, API responses, and human-readable compression reports when the runtime scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
