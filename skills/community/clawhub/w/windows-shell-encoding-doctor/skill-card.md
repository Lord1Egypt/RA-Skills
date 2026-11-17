## Description:

Helps agents diagnose and repair Windows PowerShell, cmd, and Git Bash issues involving mojibake, quoting, path spaces, JSON/stdin handling, and CRLF line endings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to help an agent diagnose Windows shell failures and produce safer PowerShell, cmd, and Git Bash commands for encoding, JSON/stdin, path, quoting, and line-ending issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested troubleshooting commands may write local UTF-8 files, change encodings, or normalize line endings.

Mitigation: Review generated commands before running them, confirm target paths, and back up important files before modifying encodings or line endings.

Risk: Shell-specific repairs can fail or behave differently if the current shell is misidentified.

Mitigation: Confirm whether the user is using PowerShell, cmd, Git Bash, MSYS, or WSL before translating commands.

## Reference(s):

- [Common Windows shell failures](references/common-failures.md)
- [Encoding checklist for Windows shell problems](references/encoding-checklist.md)
- [JSON and stdin patterns on Windows](references/json-and-stdin-patterns.md)
- [PowerShell vs Bash quick translation guide](references/powershell-vs-bash.md)
- [Repair playbooks](references/repair-playbooks.md)
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/windows-shell-encoding-doctor)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline PowerShell, cmd, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend UTF-8 file writes or line-ending normalization when needed; review generated commands before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
