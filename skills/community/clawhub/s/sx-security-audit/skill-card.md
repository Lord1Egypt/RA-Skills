## Description:

Performs broad security audits across file permissions, environment variables, dependencies, configuration files, network ports, Git settings, shell configuration, macOS security checks, and secret detection, with CLI options, JSON output, and configuration-file support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuxiaobao-y](https://clawhub.ai/user/zhuxiaobao-y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security-minded operators use this skill to run local security checks, prioritize findings, and generate Markdown or JSON audit reports. It is suited for auditing OpenClaw workspaces and nearby development environments before sharing reports or changing security posture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security reports may include shell credential values or other sensitive local findings that could be exposed if saved or shared externally.

Mitigation: Review and redact generated reports before storing them in shared locations or sending them through Feishu, webhooks, or other messaging tools.

Risk: Audit helper commands and dependency-check examples can affect the local environment if run without isolation or version pinning.

Mitigation: Run checks in an isolated environment when possible, pin tool versions before installation, and review commands before executing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuxiaobao-y/skills/sx-security-audit)
- [Permissions rules](references/permissions.md)
- [Secrets detection rules](references/secrets-detection.md)
- [Dependency vulnerability scanning](references/dependency-audit.md)
- [Code security best practices](references/code-security.md)
- [NPM Advisory Database](https://github.com/npm/advisories)
- [PyPI Security](https://pypi.org/security)
- [CVE Database](https://cve.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security)
- [Python Security Guide](https://python.readthedocs.io/en/latest/security/index.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal output, Markdown audit reports, JSON audit reports, configuration snippets, and Feishu-ready report messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include pass, warning, and fail counts, severity distribution, detailed findings, impact descriptions, and prioritized remediation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
