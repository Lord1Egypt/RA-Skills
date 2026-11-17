## Description:

Security Audit Pro helps developers run OWASP-oriented infrastructure checks with Nmap and Nikto for OpenClaw deployments, producing scan reports and hardening guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larios613-hub](https://clawhub.ai/user/larios613-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to perform authorized OpenClaw infrastructure audits, check OWASP Top 10 categories, and generate scan reports with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Active Nmap and Nikto scans can generate alerts, affect services, or reach unintended systems when targets are scoped incorrectly.

Mitigation: Run scans only against systems that are owned or explicitly authorized, confirm target values before execution, and start with narrow scopes.

Risk: The skill can overstate OWASP, hardening, and compliance coverage.

Mitigation: Treat outputs as basic scan evidence and have findings reviewed through a qualified security process before relying on them for compliance claims.

## Reference(s):

- [OWASP Top 10:2025 Audit Checklist](references/owasp-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text reports with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create timestamped local audit report files when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
