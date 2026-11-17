## Description:

Uploads and sends .md files from your OpenClaw workspace to a specific Telegram chat using the Telegram Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[courtneejay](https://clawhub.ai/user/courtneejay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace users use this skill to send selected Markdown files from an OpenClaw workspace to an intended Telegram recipient or chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A selected Markdown file may contain secrets, private business data, or other content not intended for the configured Telegram chat.

Mitigation: Review the file before upload and confirm TELEGRAM_CHAT_ID points to the intended recipient.

Risk: The included uploader script appears malformed until its indentation and documented path are fixed.

Mitigation: Fix and test the script path and Python indentation before relying on the upload workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/courtneejay/skills/telegram-md-uploader)
- [BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and a Python uploader script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads only user-selected .md files when TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are configured.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
