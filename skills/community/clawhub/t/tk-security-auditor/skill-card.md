## Description:

Run security audits on Linux servers, web applications, and cloud infrastructure. Checks SSH hardening, firewall rules, open ports, SSL/TLS config, file permissions, and common vulnerabilities. Produces actionable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tktk-ai](https://clawhub.ai/user/tktk-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, small teams, and freelancers use this skill to audit Linux servers, web applications, and cloud infrastructure, then produce prioritized security findings with suggested remediation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested remediation commands may change SSH, firewall, package, or system configuration on live infrastructure.

Mitigation: Review commands before use, keep fallback access open for SSH and firewall changes, test configuration edits first, and take backups or snapshots before applying persistent changes.

Risk: Audit results and fix guidance may be incomplete or context-dependent for a specific server, web app, or cloud environment.

Mitigation: Treat the report as a starting point for security review and verify findings against the actual target environment before relying on the recommendations.

## Reference(s):

- [Server Hardening Checklist](references/hardening-checklist.md)
- [Common Security Fix Commands](references/common-fixes.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized findings include risk level, current state, suggested fix commands, and verification steps.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
