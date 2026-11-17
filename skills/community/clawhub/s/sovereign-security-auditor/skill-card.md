## Description:

Comprehensive code security audit covering OWASP Top 10, secrets detection, dependency vulnerabilities, and language-specific attack patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to audit codebases, repositories, and pull requests for common application vulnerabilities, exposed secrets, dependency risks, and configuration weaknesses. It produces prioritized findings with impact and concrete remediation examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit may inspect configuration and secret-related files and report sensitive findings in chat.

Mitigation: Run it only on intended repositories, files, or pull requests, and avoid including files you do not want disclosed in the audit conversation.

## Reference(s):

- [OWASP Cross-Site Scripting](https://owasp.org/www-community/attacks/xss/)
- [Forge Tools](https://ryudi84.github.io/sovereign-tools/)
- [Sovereign Tools Repository](https://github.com/ryudi84/sovereign-tools)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown with structured findings and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped by severity and include category, location, impact, fix examples, and references when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
