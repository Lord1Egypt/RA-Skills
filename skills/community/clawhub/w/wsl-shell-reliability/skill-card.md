## Description:

Reliability-first shell selection policy for AI agents on Windows. Choose WSL or PowerShell based on execution risk, not preference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cikichen](https://clawhub.ai/user/cikichen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill on Windows to choose between WSL/bash and PowerShell/CMD based on execution reliability, shell semantics, and fallback risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands may delete files, alter services or registry settings, install packages, or cross between WSL and Windows paths.

Mitigation: Review high-impact commands before execution and confirm the selected shell matches the operation.

Risk: Shell fallback could accidentally change command semantics if syntax is translated carelessly.

Mitigation: Preserve the original command intent, translate only shell syntax, and state any fallback explicitly.

Risk: Windows and WSL path, quoting, line-ending, or tool-resolution differences can cause command failures.

Mitigation: Use one path style per command, quote paths with spaces, prefer deterministic WSL invocation when needed, and report environment constraints clearly.

## Reference(s):

- [Reference: Reliability Notes for Windows Terminal Execution](references/REFERENCE.md)
- [Scenarios: When to Use WSL vs PowerShell](references/SCENARIOS.md)
- [ClawHub Skill Page](https://clawhub.ai/cikichen/skills/wsl-shell-reliability)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples are shell-specific and should preserve intent across fallback.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
