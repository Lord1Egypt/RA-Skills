## Description: <br>
Lightweight task management CLI for multi-agent workflows with a SQLite backend, local task tracking, board summaries, and status-change hooks that emit agent instructions without auto-executing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckouder](https://clawhub.ai/user/ckouder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams coordinating multi-agent projects use this skill to create, assign, update, summarize, and audit tasks in a local SQLite taskboard. It can also guide optional handoffs to GitHub Issues, Discord notifications, and cron-based board checks when the user deliberately configures those integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional GitHub sync can modify remote issues or expose task details if configured with the wrong repository, assignees, or token permissions. <br>
Mitigation: Confirm the repository, issue mapping, and assignees before sync; use a dedicated least-privilege GitHub token and require confirmation before closing or modifying remote issues. <br>
Risk: Optional webhook, Discord, and cron integrations can share task status or project details with unintended channels or recipients. <br>
Mitigation: Confirm channels, webhook targets, recipients, and payload contents before enabling notifications or scheduled summaries. <br>
Risk: Status-change hooks emit instructions that another agent may act on. <br>
Mitigation: Review hook output before execution and keep hooks limited to deliberate, human-approved handoff or notification actions. <br>


## Reference(s): <br>
- [Taskboard CLI](https://clawhub.ai/ckouder/taskboard-cli) <br>
- [Taskboard CLI Setup](references/taskboard-setup.md) <br>
- [GitHub Issues Backend](references/github-backend.md) <br>
- [Webhook & Discord Integration](references/webhook-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, CLI output, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local SQLite taskboard data through the bundled CLI; optional integrations require explicit user configuration.] <br>

## Skill Version(s): <br>
3.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
