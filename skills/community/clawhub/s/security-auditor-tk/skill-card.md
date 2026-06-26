## Description: <br>
Run security audits on Linux servers, web applications, and cloud infrastructure, checking SSH hardening, firewall rules, open ports, SSL/TLS configuration, file permissions, and common vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tktk-ai](https://clawhub.ai/user/tktk-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, freelancers, and small teams use this skill to audit systems they own or are authorized to test and to receive prioritized security findings with remediation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copy-paste hardening commands can lock users out of SSH or disrupt running services. <br>
Mitigation: Review each command manually, back up configuration files, confirm console or recovery access, and test SSH, firewall, and service changes in staging when possible. <br>
Risk: Security audit reports may expose sensitive infrastructure details. <br>
Mitigation: Store generated reports securely and share them only with people authorized to see the audited environment. <br>


## Reference(s): <br>
- [Security Auditor README](README.md) <br>
- [Server Hardening Checklist](references/hardening-checklist.md) <br>
- [Common Security Fix Commands](references/common-fixes.md) <br>
- [ClawHub skill page](https://clawhub.ai/tktk-ai/security-auditor-tk) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown security audit report with prioritized findings, fix commands, and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands are examples that require manual review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
