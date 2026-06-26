## Description: <br>
Fetch Telegram chat message history via MTProto user API (Telethon). Use when needing to read old messages from any Telegram chat, group, or forum topic that the bot API can't access. Supports fetching by chat ID, forum topic/thread, message count, pagination, and JSON output. Requires one-time user login with phone number + 2FA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhlsthrm](https://clawhub.ai/user/rhlsthrm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to log in with a Telegram user account and fetch message history from chats, groups, or forum topics that the Telegram Bot API cannot read. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants reusable access to the Telegram account used during login. <br>
Mitigation: Install only if that account access is acceptable, use a trusted local terminal, and delete the session directory or revoke the Telegram session when finished. <br>
Risk: Login codes and 2FA passwords can be exposed if copied into shell history, chats, files, or other messengers. <br>
Mitigation: Handle login secrets only in a trusted local session and avoid placing them in persistent command history or external communication channels. <br>
Risk: Fetched chat history may include private or sensitive messages. <br>
Mitigation: Fetch only chats you are authorized to access and handle exported text or JSON according to the user's privacy and retention requirements. <br>


## Reference(s): <br>
- [Telegram API application setup](https://my.telegram.org/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text or JSON arrays of Telegram message records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Telethon, Telegram API credentials, and a reusable local Telegram user session under the skill directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
