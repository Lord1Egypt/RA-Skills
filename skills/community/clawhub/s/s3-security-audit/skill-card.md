## Description:

Run security audits on codebases using static analysis, dependency scanning, and manual review patterns for OWASP Top 10 risks, secrets, dependency vulnerabilities, and infrastructure misconfigurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to perform pre-deployment security reviews, dependency vulnerability checks, secrets scans, and infrastructure configuration reviews on codebases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run local audit commands that print secrets or sensitive project details.

Mitigation: Review command output before sharing it, redact secrets immediately, and run audits only in trusted local or isolated environments.

Risk: The Python dependency audit step includes an automatic unpinned pip-audit installation that can modify the user's environment.

Mitigation: Install pip-audit separately in a trusted, isolated environment or require the agent to skip automatic installation.

Risk: Grep-based static checks can produce false positives and miss logic flaws or runtime vulnerabilities.

Mitigation: Manually verify findings and use the report as one input to a broader security review rather than a replacement for professional penetration testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/s3-security-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured security audit report with findings, severity, OWASP category, impact, remediation, and recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
