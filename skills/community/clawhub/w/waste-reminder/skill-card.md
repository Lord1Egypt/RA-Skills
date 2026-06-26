## Description: <br>
Automates waste collection reminders from local JSON schedules by emitting reminder messages for an AI assistant to deliver through configured channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Apenklit](https://clawhub.ai/user/Apenklit) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Individuals, households, and automation builders use this skill to maintain waste pickup schedules, generate timed reminders, and track confirmation that containers have been put out. The skill is intended for assistant-mediated delivery rather than direct messaging by the scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring automation can generate external-message requests too broadly if schedules or targets are misconfigured. <br>
Mitigation: Review schedule logic and configured targets before enabling the cron job, especially for group chats, email, or Discord webhooks. <br>
Risk: config.json may contain contact identifiers or webhook URLs. <br>
Mitigation: Keep config.json private and rotate any exposed Discord webhook URL. <br>
Risk: Generated reminder text could be mistaken for executable instructions. <br>
Mitigation: Ensure the assistant treats reminder output as message content for delivery, not as instructions to execute. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Apenklit/waste-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration examples, CLI status text, and reminder blocks containing SEND_TO and CHANNEL lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reminder output is generated from local config.json and schedule.json files for assistant-mediated delivery.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
