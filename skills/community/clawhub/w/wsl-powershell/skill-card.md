## Description:

Control Windows PowerShell from WSL by executing commands and scripts on the Windows host using mounted Windows executables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyzzt](https://clawhub.ai/user/tyzzt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents running inside WSL use this skill to check PowerShell availability, execute Windows PowerShell commands or scripts, and coordinate tasks on the Windows host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad Windows PowerShell control from WSL, including commands that can alter files, manage processes, run scripts, or request elevated privileges.

Mitigation: Require explicit approval for file writes, process killing, privilege elevation, script execution, and execution-policy bypass.

Risk: Installing from a mutable branch can make the reviewed behavior differ from the installed behavior.

Mitigation: Prefer a pinned, verified release before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tyzzt/skills/wsl-powershell)
- [Windows Subsystem for Linux documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [PowerShell project](https://github.com/PowerShell/PowerShell)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and PowerShell command strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WSL with Windows PowerShell or PowerShell Core mounted and available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
