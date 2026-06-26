## Description: <br>
Manage and configure Telegram bots for OpenClaw, including Telegram integration setup, bot token configuration, webhook or channel settings, token validation, and connectivity checks for api.telegram.org. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[362224222](https://clawhub.ai/user/362224222) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to set up, validate, and troubleshoot Telegram bot integrations. It supports bot registration guidance, local OpenClaw configuration, webhook or polling setup, and Telegram API connectivity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens may leak through command-line arguments, shell history, terminal output, logs, screenshots, or committed configuration files. <br>
Mitigation: Use a dedicated bot token, prefer environment variables or secured configuration over command-line arguments, restrict access to config and backup files, and rotate any token that may have been exposed. <br>
Risk: Setup behavior can make local OpenClaw configuration changes and create backup files that may contain sensitive token values. <br>
Mitigation: Review the scripts before execution, run them in the intended OpenClaw environment, verify file permissions on OpenClaw config and backup files, and confirm the resulting Telegram settings before production use. <br>


## Reference(s): <br>
- [OpenClaw Telegram Configuration Guide](references/OPENCLAW_CONFIG.md) <br>
- [Telegram Webhook Setup Guide](references/WEBHOOK_SETUP.md) <br>
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api) <br>
- [BotFather Documentation](https://core.telegram.org/bots#6-botfather) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/362224222/telegram-bot-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown documentation with bash commands, JSON configuration examples, and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational steps that can call Telegram API endpoints and modify local OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
