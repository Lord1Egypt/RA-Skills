## Description: <br>
Reminder Engine is an agent skill for creating one-time, recurring, incremental, batch, multi-channel, and webhook-delivered reminders through platform scheduling commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, project managers, and assistants use this skill to turn natural-language reminder requests into scheduled reminders, recurring jobs, multi-channel notifications, and webhook-triggered follow-up tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create cron-style jobs that may persist or recur beyond the current conversation. <br>
Mitigation: Review each proposed schedule, recurrence rule, target session, and cleanup setting before allowing job creation; prefer delete-after-run for one-time reminders. <br>
Risk: Webhook delivery can send reminder content and task results to external endpoints. <br>
Mitigation: Allow only expected HTTPS webhook targets, avoid sensitive reminder content, and verify signing secrets are managed outside the skill text. <br>
Risk: The skill uses command authority and platform scheduling commands. <br>
Mitigation: Run commands in the intended agent platform only after reviewing arguments, channel identifiers, time expressions, and destructive cleanup actions. <br>
Risk: The security evidence flags broad activation language and unrelated security or file-processing claims. <br>
Mitigation: Treat security-audit and file-processing claims as unverified; use the skill only for reminder scheduling unless separately validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/reminder-engine) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or describe platform cron jobs, webhook delivery settings, channel targets, and cleanup commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
