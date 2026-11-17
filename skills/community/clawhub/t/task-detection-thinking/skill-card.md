## Description:

Incomplete task detection + proactive thinking. Automatically scans task status, identifies anomalies, generates solutions, and attempts auto-fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opendolph](https://clawhub.ai/user/opendolph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent users use this skill to scan HEARTBEAT.md and WORKING.md task records, detect stalled, blocked, overdue, duplicate, or incomplete tasks, and generate follow-up analysis and solution options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically act on task-management records, including changing task status or deadlines.

Mitigation: Keep auto-fix disabled unless explicitly needed and review proposed task changes before applying them.

Risk: Task names, blocker notes, and analysis may be persisted into memory files.

Mitigation: Avoid placing secrets, sensitive customer details, or confidential project information in task records that the skill scans or writes.

Risk: Scheduled scans and Feishu alerts can send task details without enough user control.

Mitigation: Leave scheduled scans and Feishu alerts disabled until notification scope, recipients, and data handling are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/opendolph/skills/task-detection-thinking)
- [README](README.md)
- [Skill definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and console text with task alerts, thinking logs, solution options, shell usage examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact describes writing task-alert.md and thinking-log.md under memory/hot and may trigger Feishu alerts for high-severity task issues.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
