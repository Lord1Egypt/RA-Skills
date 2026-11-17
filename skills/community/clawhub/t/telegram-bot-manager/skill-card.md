## Description:

Manage and configure Telegram bots for OpenClaw. Use when setting up Telegram integrations, troubleshooting bot connectivity, configuring bot tokens, or managing Telegram channel/webhook settings. Handles bot registration, token validation, and network connectivity checks for api.telegram.org.

This skill is ready for commercial/non-commercial use.

## Publisher:

[362224222](https://clawhub.ai/user/362224222)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to set up, test, and troubleshoot Telegram bot integrations for OpenClaw, including bot token validation, OpenClaw configuration, polling, and webhook setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens may be exposed through command-line history, process listings, configuration files, or backup files.

Mitigation: Use environment variables or owner-only secure configuration, avoid passing production tokens as command-line arguments, rotate compromised tokens, and verify OpenClaw config and backup file permissions.

Risk: Webhook setup guidance includes privileged system commands that can change nginx, firewall, certificate, and public endpoint configuration.

Mitigation: Run privileged webhook setup commands only on systems intended for those changes, review commands before execution, and confirm SSL, secret token, and access controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/362224222/skills/telegram-bot-manager)
- [OpenClaw Publisher Profile](https://clawhub.ai/user/362224222)
- [OpenClaw Telegram Configuration Guide](references/OPENCLAW_CONFIG.md)
- [Telegram Webhook Setup Guide](references/WEBHOOK_SETUP.md)
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [BotFather Documentation](https://core.telegram.org/bots#6-botfather)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that call Telegram APIs, update OpenClaw configuration, restart the OpenClaw gateway, or modify webhook infrastructure.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact metadata, release notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
