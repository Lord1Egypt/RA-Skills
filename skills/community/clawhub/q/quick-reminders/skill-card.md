## Description: <br>
Zero-LLM one-shot reminders (<48h) via nohup sleep + openclaw message send, operated via {baseDir}/scripts/nohup-reminder.sh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lstpsche](https://clawhub.ai/user/lstpsche) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and personal-assistant agents use this skill to create, list, and cancel short-horizon reminders that are delivered through a configured OpenClaw messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder text, timing metadata, and delivery targets are stored locally and sent through the configured OpenClaw messaging account. <br>
Mitigation: Avoid sensitive reminder contents, verify the channel and target before creating reminders, and use list or remove commands to review or cancel pending reminders. <br>
Risk: Short-horizon background reminders may not survive machine restarts or gateway downtime. <br>
Mitigation: Use calendar reminders or a durable scheduler for reminders two or more days away or when delivery reliability is critical. <br>


## Reference(s): <br>
- [Quick Reminders ClawHub listing](https://clawhub.ai/lstpsche/quick-reminders) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local reminder state and schedules delivery through the user's configured OpenClaw messaging account.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
