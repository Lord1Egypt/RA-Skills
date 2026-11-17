## Description:

Runs local security audits across file permissions, environment variables, dependencies, configuration, network ports, Git settings, shell configuration, macOS controls, and secret patterns, with CLI, JSON, Markdown report, configuration-file, and Feishu reporting support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13256659129](https://clawhub.ai/user/13256659129)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local security checks, review prioritized findings, and produce audit reports before sharing or remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan sensitive host data and produce reports that may expose secrets or secret prefixes.

Mitigation: Review generated reports before sharing and treat saved reports as sensitive material.

Risk: Sending reports to Feishu can disclose security findings or credentials if the webhook or plugin endpoint is not trusted.

Mitigation: Use Feishu delivery only with a trusted webhook or configured plugin endpoint.

Risk: Broad default audits may inspect more local data than intended.

Mitigation: Prefer explicit check selections and configure exclusions before running in sensitive workspaces.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/13256659129/skills/sx-security-audit-1-0-0)
- [Permissions rules](references/permissions.md)
- [Secrets detection rules](references/secrets-detection.md)
- [Dependency audit guidance](references/dependency-audit.md)
- [Code security best practices](references/code-security.md)
- [NPM Advisory Database](https://github.com/npm/advisories)
- [PyPI Security](https://pypi.org/security)
- [CVE Database](https://cve.mitre.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown or JSON reports with CLI output and optional Feishu message payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include summaries, risk counts, detailed findings, and prioritized remediation suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
