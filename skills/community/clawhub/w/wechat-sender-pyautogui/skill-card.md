## Description:

Uses PyAutoGUI to help an agent send WeChat messages or enter local file paths by driving the desktop client with keyboard shortcuts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anananangela](https://clawhub.ai/user/anananangela)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs to prepare or send a WeChat message to a named contact through the local desktop client. It supports message entry, local file-path entry, recipient selection by index, a no-send confirmation mode, and configurable WeChat launch hotkeys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyboard-driven automation can send a message to the wrong WeChat chat if contact selection or focus is incorrect.

Mitigation: Use --no-send by default and manually verify the selected chat before pressing Enter.

Risk: Sensitive message text or local file paths may be entered into WeChat during automation.

Mitigation: Avoid sensitive messages and paths unless the recipient and content have been confirmed.

Risk: The --file option types the path into the chat rather than attaching the file.

Mitigation: Do not rely on --file for attachment behavior; verify the result manually before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anananangela/skills/wechat-sender-pyautogui)
- [Publisher profile](https://clawhub.ai/user/anananangela)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that automate local keyboard input in WeChat; no-send mode should be preferred for confirmation-sensitive use.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
