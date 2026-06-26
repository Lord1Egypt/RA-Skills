## Description: <br>
Helps agents provide shell-specific Windows command guidance, distinguish PowerShell from cmd.exe, and rewrite Bash-style syntax safely for Windows users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loevery](https://clawhub.ai/user/loevery) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and coding agents use this skill when producing terminal commands for Windows users or translating Bash examples to PowerShell, cmd.exe, Git Bash, or WSL. It helps avoid incorrect shell assumptions, quoting mistakes, environment-variable errors, and version-specific command-chaining failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell-command guidance can still produce commands that delete, move, overwrite, or otherwise change local data if accepted without review. <br>
Mitigation: Review generated commands before execution, especially examples involving deletion, moves, redirection, overwrites, chained commands, or privileged operations. <br>
Risk: Incorrectly assuming a Windows shell can cause commands to fail or behave differently, especially for quoting, environment variables, redirection, and && / || support. <br>
Mitigation: Confirm whether the user is running cmd.exe, Windows PowerShell 5.1, PowerShell 7+, Git Bash, or WSL, and provide labeled variants when the shell is unclear. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loevery/windows-shell-syntax) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/loevery) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with labeled shell-specific command examples and concise explanatory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Labels PowerShell, PowerShell 5.1, PowerShell 7+, cmd.exe, Bash, Git Bash, or WSL variants when syntax differs.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
