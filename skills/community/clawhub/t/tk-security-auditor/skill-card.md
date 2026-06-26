## Description: <br>
Run security audits on Linux servers, web applications, and cloud infrastructure by checking SSH hardening, firewall rules, open ports, SSL/TLS configuration, file permissions, and common vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tktk-ai](https://clawhub.ai/user/tktk-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and small teams use this skill to audit Linux servers, web applications, and cloud infrastructure, then produce prioritized findings with fix commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security checks or scans could be run outside an authorized scope. <br>
Mitigation: Define the audit scope before use and run checks only on systems the operator owns or has permission to test. <br>
Risk: Copy-paste hardening commands can disrupt live services or lock out administrators, especially SSH and firewall changes. <br>
Mitigation: Review each command, prepare backups and rollback steps, schedule a maintenance window, and confirm alternate access before applying production changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tktk-ai/tk-security-auditor) <br>
- [Hardening Checklist](references/hardening-checklist.md) <br>
- [Common Security Fix Commands](references/common-fixes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, Security analysis] <br>
**Output Format:** [Markdown security audit report with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritized findings grouped by risk level with verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
