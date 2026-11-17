## Description:

Automates and assists WeChat desktop replies on macOS by finding a contact or group chat, using OCR when needed, pasting a prepared or suggested reply, and sending it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjunlei1989-glitch](https://clawhub.ai/user/chenjunlei1989-glitch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers on macOS use this skill to automate sending WeChat messages and to generate OCR-based suggested replies for desktop chats after configuring local permissions and dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control WeChat, the clipboard, screen capture, and message sending, which could send unintended messages or expose private chat content.

Mitigation: Install only after accepting those permissions, test first with File Transfer Assistant or a test contact, and avoid auto-send where possible.

Risk: OCR and UI automation depend on local WeChat layout, macOS permissions, and screen state, so contact or group selection may be unreliable across environments.

Mitigation: Run a basic local validation after installation and recalibrate click areas or single-chat/group-chat paths when the WeChat version, window size, or display layout differs.

Risk: OCR screenshots and logs may contain private chat data.

Mitigation: Treat generated screenshots and log output as sensitive local data and remove temporary files after testing.

Risk: The Homebrew installation path uses a third-party tap/formula.

Mitigation: Review the tap and formula before installation or upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjunlei1989-glitch/skills/wechat-auto-reply-mac)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and user-facing message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local macOS WeChat, Accessibility permissions, clipboard access, screen capture, cliclick, and macOS Vision OCR dependencies.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
