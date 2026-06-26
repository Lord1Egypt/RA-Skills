## Description: <br>
Prompts for confirmation, then restarts QClaw on Windows by gracefully closing running QClaw processes and relaunching the application. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenguangwu](https://clawhub.ai/user/chenguangwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QClaw users and developers use this skill when they need an agent-assisted restart after configuration changes or when explicitly asking QClaw to restart itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restarting QClaw interrupts the current session and may affect unsaved work. <br>
Mitigation: Ask for explicit confirmation that names QClaw, advise the user to save work first, and run the restart only on Windows when QClaw is already running. <br>


## Reference(s): <br>
- [QClaw Restart on ClawHub](https://clawhub.ai/chenguangwu/qclaw-restart) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with PowerShell command and script blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only; requires explicit user confirmation and an already running QClaw process.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
