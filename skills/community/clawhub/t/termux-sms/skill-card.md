## Description:

Send SMS text messages directly from the user's Android device using the Termux API when the agent is running in Termux or has remote command access to an Android device with Termux installed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryshane1983-tech](https://clawhub.ai/user/jerryshane1983-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to prepare SMS-sending commands on an Android device through Termux. It is intended for explicit user-requested texting workflows where the recipient and message are confirmed before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied recipient or message text could become shell execution if interpolated into a shell command.

Mitigation: Pass the phone number and message as separate process arguments when possible; otherwise validate recipients and apply robust shell escaping before execution.

Risk: An agent could send an unintended SMS or message the wrong recipient.

Mitigation: Require an explicit phone number and confirm the exact recipient and message text with the user before sending.

Risk: The skill can be misused for bulk or unwanted SMS messages.

Mitigation: Do not use it for spam or bulk messaging, and restrict use to specific user-requested messages.

## Reference(s):

- [ClawHub Termux SMS release page](https://clawhub.ai/jerryshane1983-tech/skills/termux-sms)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Termux API command line utility `termux-sms-send` on an Android device with SMS permission.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
