## Description:

Automates Windows desktop interactions by simulating mouse and keyboard input, managing the clipboard, taking screenshots, launching applications, running commands, and reporting system information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjx378](https://clawhub.ai/user/hjx378)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to let an agent control a Windows desktop session for GUI workflows, application launching, clipboard tasks, screenshots, and command execution. It is best suited to supervised automation where the user can confirm sensitive actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run PowerShell commands, launch applications, control the GUI, read the clipboard, and capture screenshots.

Mitigation: Require explicit user confirmation before commands or actions that modify files, access private data, use the network, install software, or interact with privileged applications.

Risk: The artifact disables the PyAutoGUI failsafe, reducing the user's ability to interrupt unintended mouse or keyboard automation.

Mitigation: Prefer a reviewed version that keeps the PyAutoGUI failsafe enabled or adds an equivalent emergency stop before deployment.

Risk: Unrestricted command execution can run arbitrary PowerShell input.

Mitigation: Use an allowlist for permitted commands and review command strings before execution.

Risk: Clipboard reads and screenshots may expose private information from the active Windows session.

Mitigation: Document screenshot and clipboard handling and require consent before collecting or sharing screen or clipboard contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hjx378/skills/windows-automation)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with code examples, command strings, file paths, and structured status values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can cause desktop side effects such as GUI input, application launch, command execution, clipboard changes, and screenshot file creation.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
