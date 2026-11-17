## Description:

Manage Telegram from an agent through a Python/Telethon CLI for user-account messaging, chat search, group and channel administration, profile actions, media transfer, and listening workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youziyouzishu](https://clawhub.ai/user/youziyouzishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and operate a Telethon-backed CLI for Telegram user-account workflows when bot API access is not appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for durable Telegram account-level access and can perform sensitive messaging, deletion, administration, block, join or leave, profile, and listen operations.

Mitigation: Use a separate Telegram profile when possible and require explicit user confirmation before any sensitive Telegram operation.

Risk: Telegram API credentials and local session files can expose account access if stored in shared repositories or left unprotected.

Mitigation: Keep API credentials out of TOOLS.md and shared repositories, and protect or remove ~/.tgctl-telethon sessions when finished.

Risk: The submitted package is incomplete because the installer references a missing tgctl script.

Mitigation: Confirm the executable script is present and reviewed before installing or using the skill.

## Reference(s):

- [Telegram API Development](https://my.telegram.org)
- [ClawHub skill page](https://clawhub.ai/youziyouzishu/skills/telegram-telethon)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI usage tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require interactive Telegram login and local session state.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
