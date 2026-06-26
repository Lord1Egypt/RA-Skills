## Description: <br>
Manage Telegram through the tgctl-telethon CLI using Python and Telethon for user-account actions including messaging, chat search, group management, media transfer, profile updates, and message listening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youziyouzishu](https://clawhub.ai/user/youziyouzishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate a Telethon-based CLI for Telegram user-account workflows. It supports tasks such as sending or editing messages, browsing chats, transferring media, managing groups and channels, and updating account state after the user has configured credentials and logged in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad powers over a real Telegram user account, including sending, deleting, joining, leaving, inviting, kicking, blocking, changing admins, updating profiles, and listening to chats. <br>
Mitigation: Require explicit user confirmation before account-changing or privacy-sensitive Telegram actions. <br>
Risk: Telegram API credentials and local session files can grant account access if exposed. <br>
Mitigation: Keep API credentials and session files private, and do not store them in shared documentation, logs, or version control. <br>
Risk: The server security verdict is suspicious because the skill is powerful account automation with limited built-in safety guidance. <br>
Mitigation: Install only when the operator intends to let an agent control a Telegram user account, and review intended commands before execution. <br>


## Reference(s): <br>
- [Telegram API Development](https://my.telegram.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/youziyouzishu/telegram-telethon) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Telegram API credentials, interactive login, and a local Telethon session before account actions can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
