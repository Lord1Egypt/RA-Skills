## Description:

Wraps sending a Telegram message to a fixed topic into one script call for quick notifications or messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shing19](https://clawhub.ai/user/shing19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send plain-text Telegram topic notifications through a configured OpenClaw channel, with chat, topic, and channel defaults that can be overridden per call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can send a message to an unintended Telegram destination if channel, chat ID, topic ID, or configured OpenClaw channel auth are wrong.

Mitigation: Confirm the configured OpenClaw channel auth and verify --channel, --chat-id, and --topic-id before running the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shing19/skills/telegram-topic-message-sender)
- [Publisher profile](https://clawhub.ai/user/shing19)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [Markdown with inline bash commands and plain-text messaging guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends user-provided plain text through OpenClaw messaging; markdown and HTML parse modes are intentionally not enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
