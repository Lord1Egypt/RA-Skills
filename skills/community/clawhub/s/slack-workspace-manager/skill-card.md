## Description: <br>
Slack Workspace Manager helps Slack workspace and Enterprise Grid administrators manage teams, audit logs, Canvas documents, user groups, channels, permissions, custom emoji, and calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Slack workspace, Enterprise Grid, IT, security, and compliance administrators use this skill to plan and carry out Slack administration tasks such as bulk channel setup, user group management, Canvas updates, audit-log review, and workspace permission checks. Because these workflows can affect users, permissions, channels, and audit data, use it only for explicit administrative tasks with review before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad routing language may cause non-administrative or unrelated work to be routed to a skill capable of high-impact Slack workspace changes. <br>
Mitigation: Install and invoke it only for explicit Slack workspace or Enterprise Grid administration tasks, and review each requested action before execution. <br>
Risk: Bulk or destructive Slack operations can change channels, memberships, permissions, Canvas content, or audit workflows at scale. <br>
Mitigation: Require dry-run previews and explicit confirmation for bulk, archival, deletion, permission, or membership changes. <br>
Risk: Slack tokens and administrative credentials can expose sensitive workspace access if overprivileged or mishandled. <br>
Mitigation: Use least-privilege Slack tokens, store credentials outside source control, and rotate tokens when access requirements change. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/slack-workspace-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, Python, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include administrative action plans, command examples, structured JSON responses, and safety checks such as dry-run or confirmation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
