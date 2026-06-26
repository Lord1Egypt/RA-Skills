## Description: <br>
Automates Windows desktop interactions by simulating mouse and keyboard input, capturing screenshots, managing clipboard text, launching applications, running local commands, and reporting basic system information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HJx378](https://clawhub.ai/user/HJx378) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this skill to automate local Windows GUI workflows, inspect screen and cursor state, move text through the clipboard, launch applications, and execute PowerShell or cmd commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent Windows desktop control, screenshots, clipboard access, application launch capability, and unrestricted local command execution as the current user. <br>
Mitigation: Install only when that level of local control is intended, require explicit approval before screenshots, clipboard reads, app launches, or shell commands, and avoid sensitive financial, administrative, credential, or destructive workflows without separate safeguards. <br>
Risk: The mouse failsafe is disabled, so automated pointer movement and clicks may be harder to interrupt if the agent acts unexpectedly. <br>
Mitigation: Keep a separate interruption path available before running automation and review planned mouse and keyboard actions before execution. <br>
Risk: Clipboard and screenshot operations can expose sensitive visible information or copied text to the agent. <br>
Mitigation: Clear sensitive windows and clipboard contents before use and approve each operation that reads the screen or clipboard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HJx378/windows-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code examples and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool functions return strings, dictionaries, or screenshot files depending on the operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
