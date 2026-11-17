## Description:

Prompts for confirmation before restarting QClaw on Windows by gracefully closing running QClaw processes, waiting, and relaunching the executable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenguangwu](https://clawhub.ai/user/chenguangwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QClaw users use this skill when configuration changes require restarting the QClaw desktop app or when the user explicitly asks the agent to restart it. It is limited to Windows workspaces where QClaw is already running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a PowerShell restart script from the workspace without verifying that the script is the intended one.

Mitigation: Use only in trusted workspaces and regenerate or verify restart-qclaw.ps1 before execution.

Risk: Restarting QClaw interrupts the current session and may force-stop unresponsive QClaw processes.

Mitigation: Ask for explicit user confirmation before restarting and allow graceful CloseMainWindow shutdown before any force stop.

Risk: The restart flow is Windows-only and requires QClaw to already be running.

Mitigation: Check the operating system and confirm a running QClaw process before invoking the restart command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenguangwu/skills/qclaw-restart)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown instructions with PowerShell code block and command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; requires explicit user confirmation and a running QClaw process.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
