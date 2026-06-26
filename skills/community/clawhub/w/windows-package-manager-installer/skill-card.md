## Description: <br>
Installs Windows applications and sets up winget or Chocolatey package-manager environments with commands, verification steps, and clear status summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darkqiank](https://clawhub.ai/user/darkqiank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Windows users, administrators, and developers use this skill to choose between winget and Chocolatey, install Windows software, repair or install package managers, configure Chocolatey sources, and verify the resulting environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-manager commands can install or modify system software and may require administrator privileges. <br>
Mitigation: Review each command before execution and confirm it matches official package-manager documentation or a trusted source. <br>
Risk: Changing Chocolatey sources to a mirror can affect future package resolution and trust assumptions. <br>
Mitigation: Confirm the final Chocolatey source list after configuration and avoid changing package sources unless the user understands how to restore defaults. <br>
Risk: Exact package IDs or package availability may be incorrect if they are guessed instead of verified. <br>
Mitigation: Search winget or Chocolatey first, then use exact package identifiers only when the current conversation or command output establishes them. <br>


## Reference(s): <br>
- [Package Manager Selection Notes](references/package-selection.md) <br>
- [Chocolatey Community Install Script](https://community.chocolatey.org/install.ps1) <br>
- [Tsinghua Chocolatey Mirror](https://mirrors.tuna.tsinghua.edu.cn/chocolatey/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ends with concise Chinese success, partial-completion, or failure status messaging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
