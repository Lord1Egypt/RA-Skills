## Description: <br>
Winskill helps an agent provide Windows server operations guidance for diagnostics, read-only audits, and confirmation-gated maintenance using PowerShell. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyniujin](https://clawhub.ai/user/fyniujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and operations engineers use this skill to inspect Windows server health, disk usage, services, IIS, updates, event logs, installed software, network activity, and user sessions. It is intended to help an agent propose diagnostic PowerShell and require confirmation before maintenance actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maintenance actions such as cleanup, rename or move operations, service restarts, log export, update-cache cleanup, or long-running performance collection can change system state or affect availability. <br>
Mitigation: Require explicit user confirmation before running any state-changing command, show the planned operation first, and review generated PowerShell before execution as Administrator. <br>
Risk: Diagnostics may expose local administration data such as event logs, installed software, network connections, user sessions, or security audit results. <br>
Mitigation: Use the skill only on Windows systems where local inspection is acceptable, avoid sharing sensitive outputs unnecessarily, and confirm before exporting logs or reports. <br>
Risk: Some checks or maintenance steps require elevated Windows privileges and may fail or behave differently without them. <br>
Mitigation: Run elevated commands only when the requested operation needs them, and prefer read-only diagnostics before attempting confirmed maintenance actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fyniujin/skills/winskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require Windows PowerShell 5.1+ and administrator privileges for selected diagnostics or maintenance actions.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
