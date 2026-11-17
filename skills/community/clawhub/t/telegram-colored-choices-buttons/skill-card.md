## Description:

Automatically colors Telegram bot choice buttons as default, destructive, or secondary based on action criticality and reversibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandysuper](https://clawhub.ai/user/dandysuper)

### License/Terms of Use:


## Use Case:

Developers building Telegram bots use this skill to classify multi-choice buttons by consequence and generate button payloads or helper code with appropriate default, destructive, and secondary styling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bot tokens can be exposed if passed through shell history, process lists, logs, or committed environment files.

Mitigation: Provide BOT_TOKEN through protected environment handling, keep .env out of version control, and avoid printing or storing secrets in shared logs.

Risk: Generated dependency constraints allow newer package versions, which can change behavior over time.

Mitigation: Pin dependency versions before production use and review updates during maintenance.

Risk: The helper scripts can send Telegram test messages to the configured chat.

Mitigation: Confirm the bot token and chat ID before execution, and test in a dedicated chat before using production channels.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dandysuper/skills/telegram-colored-choices-buttons)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Bot API Changelog](https://core.telegram.org/bots/api-changelog)
- [Telegram Blog Announcement](https://telegram.org/blog/crafting-android-design-and-more)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold a Telegram bot project with a .env template, requirements file, and Python helper module.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
