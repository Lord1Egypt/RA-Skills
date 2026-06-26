## Description: <br>
Sends local workspace files to Telegram chats through the Telegram Bot API, supporting documents, photos, videos, audio, and other media with path, size, and token-handling guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bustes01](https://clawhub.ai/user/bustes01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to deliver a selected workspace file to a Telegram chat when the user explicitly requests Telegram delivery. The skill resolves and validates the file path, chooses the appropriate Telegram send method, and reports Telegram API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A selected workspace file can be sent outside the workspace to Telegram. <br>
Mitigation: Verify the exact file and Telegram destination before sending, and avoid sending source code, secrets, or private documents unless external sharing is intended. <br>
Risk: The Telegram bot token can authorize file delivery if exposed. <br>
Mitigation: Read the token only from TG_BOT_TOKEN, treat it like a password, and never log, echo, or hardcode it. <br>
Risk: Incorrect path handling could send the wrong file or allow traversal outside the workspace. <br>
Mitigation: Resolve paths with realpath, reject symlinks and files outside the workspace, require the file to exist, and enforce Telegram size limits before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bustes01/tg-file-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash curl examples and Telegram API response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and TG_BOT_TOKEN; uses workspace path validation and Telegram file size checks before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
