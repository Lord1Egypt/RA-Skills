## Description:

Send files quickly via Telegram using the tsend CLI tool with optional captions, profiles, and simple token/chat ID configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shingwha](https://clawhub.ai/user/shingwha)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and run the tsend CLI for sending documents, images, multiple files, or short messages to a configured Telegram chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens and chat IDs can grant access to send data through the configured bot.

Mitigation: Prefer TSEND_TOKEN and TSEND_CHAT_ID environment variables, and restrict ~/.tsend/config.json to the local user if a config file is used.

Risk: Files and messages sent with the CLI leave the local machine and are transmitted to Telegram.

Mitigation: Use dry-run previews, verify the destination chat, and avoid sending sensitive documents unless Telegram is the intended destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shingwha/skills/tsend)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide installation, profile configuration, dry-run previews, and Telegram file or message sending.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
