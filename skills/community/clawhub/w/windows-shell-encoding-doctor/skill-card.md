## Description: <br>
诊断修复 Windows 下 PowerShell/cmd/Git Bash 的乱码、引号转义、路径空格与 CRLF 等问题。当用户说：PowerShell 里跑 bash 命令报错、中文乱码怎么修、JSON 怎么安全传给命令行，或类似 Windows 终端编码问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose and repair Windows PowerShell, cmd.exe, Git Bash, encoding, quoting, path, JSON, stdin, and line-ending issues. It helps translate shell-specific commands into safer Windows-native patterns and explains the likely root cause. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested repair commands may write files, change encodings, or normalize line endings. <br>
Mitigation: Review commands before running them, keep backups for important files, and prefer reversible file-based fixes when working with user data. <br>
Risk: Shell translation advice can be misapplied if the user is running a different Windows shell than assumed. <br>
Mitigation: Identify whether the current shell is PowerShell, cmd.exe, Git Bash, MSYS, or WSL before applying translated commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/windows-shell-encoding-doctor) <br>
- [Common Windows shell failures](references/common-failures.md) <br>
- [Encoding checklist for Windows shell problems](references/encoding-checklist.md) <br>
- [JSON and stdin patterns on Windows](references/json-and-stdin-patterns.md) <br>
- [PowerShell vs Bash quick translation guide](references/powershell-vs-bash.md) <br>
- [Repair playbooks](references/repair-playbooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline PowerShell, cmd, bash, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include copy-pasteable commands, file-based repair patterns, and concise root-cause explanations.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
