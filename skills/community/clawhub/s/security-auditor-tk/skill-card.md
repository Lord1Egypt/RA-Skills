## Description:

Runs security audits on Linux servers, web applications, and cloud infrastructure, checking hardening, exposure, SSL/TLS, file permissions, updates, and common vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tktk-ai](https://clawhub.ai/user/tktk-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, small teams, and freelancers use this skill to audit Linux servers, web applications, and cloud infrastructure before deployment or during routine hardening. It helps produce prioritized findings, remediation commands, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remediation commands can change SSH, firewall, mount, service, or kernel settings and may cause lockout or service disruption.

Mitigation: Treat commands as proposals for experienced administrators; require backups, active fallback access, target-specific validation, and rollback steps before production execution.

Risk: Audit findings and fixes can be incomplete or environment-specific.

Mitigation: Confirm findings with system logs, package managers, cloud consoles, and approved security tools before accepting risk ratings or closing issues.

## Reference(s):

- [Server Hardening Checklist](references/hardening-checklist.md)
- [Common Security Fix Commands](references/common-fixes.md)
- [ClawHub skill page](https://clawhub.ai/tktk-ai/skills/security-auditor-tk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown security audit report with inline bash and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes prioritized findings, remediation commands, risk levels, passed checks, and verification steps.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
