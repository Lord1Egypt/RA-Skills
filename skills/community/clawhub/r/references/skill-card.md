## Description:

References is a security-audit skill that helps agents check file permissions, environment variables, dependencies, configuration, network ports, Git history, shell settings, macOS controls, and secret patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13256659129](https://clawhub.ai/user/13256659129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and operations teams use this skill to run local security checks and receive audit reports with prioritized remediation guidance. It is intended for reviewing local OpenClaw/workspace configuration, code, dependencies, credentials exposure, and host security posture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local audit reports may include sensitive local paths, configuration details, environment-variable names, or possible secret fragments.

Mitigation: Review and redact generated reports before sharing, storing, or sending them through Feishu, webhooks, or other external channels.

Risk: The release bundles unrelated reminder and payment scripts, including an exposed WeCom webhook key, which broadens behavior beyond security auditing.

Mitigation: Remove or ignore unrelated scripts before installation and treat the exposed webhook key as compromised.

Risk: Report delivery through Feishu plugin APIs or webhooks can duplicate sensitive audit data outside the local workspace.

Mitigation: Run audits locally by default and enable report delivery only with approved destinations after the report has been reviewed.

## Reference(s):

- [Permissions Check Rules](artifact/permissions.md)
- [Secret Detection Rules](artifact/secrets-detection.md)
- [Dependency Vulnerability Scanning](artifact/dependency-audit.md)
- [Code Security Best Practices](artifact/code-security.md)
- [NPM Advisory Database](https://github.com/npm/advisories)
- [PyPI Security](https://pypi.org/security)
- [CVE Database](https://cve.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown or JSON audit reports with summaries, findings, severity counts, and remediation commands; optional Feishu-formatted message text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include local paths and possible secret fragments, so review and redact before storing or sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
