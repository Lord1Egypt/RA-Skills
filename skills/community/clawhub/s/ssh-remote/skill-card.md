## Description:

Connects agents to remote Linux servers through SSH for non-interactive login, command execution, password or key authentication, and file transfer across Windows Git Bash, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agilebuilder](https://clawhub.ai/user/agilebuilder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to propose SSH connection commands, execute remote Linux commands non-interactively, transfer files, or set up SSH key-based access. It is intended for operational SSH workflows where users can review commands before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples that bypass host key checking can expose SSH sessions to host impersonation or man-in-the-middle attacks.

Mitigation: Prefer verified known_hosts entries, confirm host fingerprints for first-time connections, and reserve host-key bypass options for temporary access where the user accepts the risk.

Risk: Password-based examples can leak credentials through temporary scripts, command history, process listings, or copied production use.

Mitigation: Prefer SSH keys managed by an agent, avoid hard-coding passwords, remove temporary password files immediately, and review credential-handling commands before execution.

Risk: Remote SSH guidance can create or modify persistent access on target systems.

Mitigation: Use non-root accounts where possible, scope commands to the intended host and account, and review proposed remote commands before running them.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/agilebuilder/dev-skills/tree/master/skills/ssh-remote)
- [ClawHub skill page](https://clawhub.ai/agilebuilder/skills/ssh-remote)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SSH options, known_hosts guidance, authentication setup, file transfer commands, and security caveats.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
