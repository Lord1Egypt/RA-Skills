## Description: <br>
Manages a Telegram userbot autopilot that responds to private messages as the user using AI, with contact whitelisting, configurable response style, owner notifications, and optional paid-media support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shor73](https://clawhub.ai/user/Shor73) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and operate a personal Telegram account autopilot that can reply to approved private contacts, maintain conversational context, and send messages or media as the account owner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A long-running AI userbot can read private Telegram messages and send messages as the account owner. <br>
Mitigation: Use a narrow contact whitelist, avoid sensitive chats, disclose automation where appropriate, and review conversations regularly. <br>
Risk: Telegram session files, configuration files, history files, API keys, phone credentials, and 2FA secrets can grant access to accounts or providers. <br>
Mitigation: Protect these files like passwords, never commit them, restrict filesystem access, and avoid passing 2FA secrets on the command line. <br>
Risk: Owner notifications may forward private messages through a Telegram bot. <br>
Mitigation: Enable notifications only with a bot token and chat that the account owner fully controls. <br>
Risk: Automating Telegram replies may create consent, transparency, or platform-policy risk. <br>
Mitigation: Use the skill only where automation is appropriate, keep response behavior conservative, and monitor Telegram account restrictions or rate limits. <br>


## Reference(s): <br>
- [Telegram Authentication Flow](references/telegram-auth.md) <br>
- [Telegram API authentication](https://core.telegram.org/api/auth) <br>
- [Telegram paid media API](https://core.telegram.org/api/paid-media) <br>
- [Telegram API development tools](https://my.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and Python script usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operation guidance for Telegram credentials, session files, contact whitelists, AI provider settings, owner notifications, and optional paid-media workflows.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
