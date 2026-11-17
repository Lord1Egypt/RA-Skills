## Description:

Provides Windows shell syntax guidance that helps agents distinguish PowerShell, cmd.exe, and Unix-style shells before suggesting commands or rewrites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loevery](https://clawhub.ai/user/loevery)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when answering Windows terminal questions, converting Bash snippets to PowerShell or cmd.exe, and avoiding shell compatibility mistakes around quoting, chaining, environment variables, and line continuation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated command examples can still be unsafe when they involve file deletion, environment changes, or other consequential operations.

Mitigation: Review commands before execution and keep shell-specific variants clearly labeled so users can choose the command for their actual shell.

Risk: Ambiguous Windows shell context can produce incorrect syntax, especially across cmd.exe, Windows PowerShell 5.1, and PowerShell 7+.

Mitigation: Ask for the shell and version when needed, or provide separate labeled variants and use PowerShell 5.1-compatible guarded logic when the version is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loevery/skills/windows-shell-syntax)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code]

**Output Format:** [Markdown with concise prose and labeled shell-specific command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include separate PowerShell, PowerShell 5.1, PowerShell 7+, cmd.exe, Bash, Git Bash, or WSL variants when syntax differs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
