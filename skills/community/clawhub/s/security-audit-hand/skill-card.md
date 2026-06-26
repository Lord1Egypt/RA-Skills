## Description: <br>
Autonomous security audit skill for regularly checking system security, finding risks, and generating reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bandwe](https://clawhub.ai/user/Bandwe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw and server security posture, review configurations, analyze logs, score risks, and generate remediation-focused audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit runs may expose local secrets, logs, workspace metadata, process state, network information, or system configuration details. <br>
Mitigation: Require explicit approval for each audit run, redact secrets from reports and notifications, and remove commands that print API keys or token values. <br>
Risk: Scheduled audits may collect or retain sensitive reports without clear consent or retention controls. <br>
Mitigation: Keep scheduled audits disabled unless report storage location, retention period, access control, and notification handling are clearly configured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bandwe/security-audit-hand) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown security audit report with shell commands, configuration snippets, risk scores, and remediation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include audit checklists, dashboard metrics, historical trend comparisons, and scheduled audit settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
