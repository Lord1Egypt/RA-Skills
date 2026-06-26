## Description: <br>
Automatically scans task status, identifies anomalies, generates solutions, and attempts auto-fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opendolph](https://clawhub.ai/user/opendolph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor OpenClaw task boards, detect stalled, blocked, overdue, duplicate, or incomplete tasks, and produce proactive analysis with solution options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read task boards and create persistent memory logs containing project status, deadlines, owners, dependencies, and block reasons. <br>
Mitigation: Install it only in workspaces where the agent is allowed to process that project data, and review generated memory files before sharing or syncing them. <br>
Risk: Auto-fix behavior may change task status, deadlines, or schedules without enough human approval. <br>
Mitigation: Keep auto-fix and schedule adjustment disabled unless each action is explicitly approved. <br>
Risk: Critical alerts may send task details to Feishu. <br>
Mitigation: Keep Feishu alerts disabled until the destination, recipients, and data-sharing rules are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/opendolph/task-detection-thinking) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown task alerts and thinking logs with shell command examples and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes detection results to memory/hot/task-alert.md, appends thinking logs to memory/hot/thinking-log.md, and may prepare Feishu alerts for critical issues.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
