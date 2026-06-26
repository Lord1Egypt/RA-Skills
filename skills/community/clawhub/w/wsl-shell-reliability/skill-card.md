## Description: <br>
Reliability-first shell selection policy for AI agents on Windows. Choose WSL or PowerShell based on execution risk, not preference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cikichen](https://clawhub.ai/user/cikichen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents working on Windows use this skill to choose between WSL/bash and PowerShell/CMD based on execution risk, command semantics, and fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent toward commands that install software, delete files, or change system settings. <br>
Mitigation: Review commands before execution, especially destructive or system-changing commands. <br>
Risk: Switching between WSL and PowerShell can change quoting, path handling, or tool resolution. <br>
Mitigation: Require explicit fallback reporting and preserve command intent when translating syntax. <br>


## Reference(s): <br>
- [Reliability Notes for Windows Terminal Execution](references/REFERENCE.md) <br>
- [Scenarios: When to Use WSL vs PowerShell](references/SCENARIOS.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cikichen/wsl-shell-reliability) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell command templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Explains shell selection, syntax translation, and explicit fallback reporting for Windows terminal tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
