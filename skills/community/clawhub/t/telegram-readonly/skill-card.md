## Description: <br>
Read the user's personal Telegram account in a controlled, read-only way via Telethon/MTProto for inspecting chats, listing dialogs, reading recent messages, and searching messages without using the Telegram Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ropl-btc](https://clawhub.ai/user/ropl-btc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need controlled, local, read-only access to a user's personal Telegram account for chat inspection, dialog listing, recent-message retrieval, or targeted message search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a reusable full-account Telegram session, so compromise of the local session config can enable continued account access. <br>
Mitigation: Treat ~/.config/telegram-readonly/config.json like a password, restrict local access to it, revoke the Telegram session or delete the config when no longer needed, and avoid exposing the session string in logs or shared outputs. <br>
Risk: The documented installation path can install external GitHub code without a pinned commit. <br>
Mitigation: Review the exact code before authenticating and pin a trusted commit or package version for repeatable installation. <br>
Risk: Broad Telegram reads or exports can expose sensitive personal or third-party conversations. <br>
Mitigation: Use small, specific reads, prefer targeted chats or searches, and ask before broad history exports or background monitoring. <br>
Risk: Unread-state preservation is best effort and may vary with Telegram client behavior. <br>
Mitigation: Test on a low-risk chat before broad use and stop if the wrapper changes unread state unexpectedly. <br>


## Reference(s): <br>
- [Setup and safety](references/setup-and-safety.md) <br>
- [Telegram API development tools](https://my.telegram.org) <br>
- [ClawHub skill page](https://clawhub.ai/ropl-btc/telegram-readonly) <br>
- [Publisher profile](https://clawhub.ai/user/ropl-btc) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; the Telegram CLI returns JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Telegram operations; session handling requires user-controlled credentials and local configuration.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
