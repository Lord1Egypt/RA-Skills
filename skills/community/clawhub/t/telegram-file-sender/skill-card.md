## Description: <br>
Send local files and documents to a Telegram user via a bot, with path handling and 50MB size-limit zipping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daowuu](https://clawhub.ai/user/daowuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user asks to send a local file, note, or document to Telegram through a configured bot. It prepares the selected file path, handles Telegram's 50MB document limit, and provides the values needed for the Telegram message send action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare any readable local file path for transfer to Telegram. <br>
Mitigation: Before each send, verify the exact source path, destination chat ID, and bot accountId, and avoid secrets, credentials, private system files, or files the user has not explicitly chosen to share. <br>
Risk: A file may be sent to the wrong Telegram chat or through the wrong bot account if identifiers are misconfigured. <br>
Mitigation: Confirm the target user's Telegram chat ID and bot accountId before invoking the message send action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daowuu/telegram-file-sender) <br>
- [Skill Homepage](https://clawhub.ai/skills/telegram-file-sender) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, key-value helper output, and a JSON message-tool payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper output includes SEND_PATH, SEND_FILENAME, TARGET, CAPTION, ACCOUNT_ID, and READY for agent parsing.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
