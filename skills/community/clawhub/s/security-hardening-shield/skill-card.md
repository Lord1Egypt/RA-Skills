## Description:

安全加固之盾 helps agents inspect software projects for OWASP Top 10 risks, trust/data/network boundary issues, authentication weaknesses, secret handling gaps, and dependency vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and automation teams use this skill to profile a codebase, classify security boundaries, check common web application risks, and produce remediation-oriented audit reports before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to inspect code and run security scanner commands, which may be too broad for unattended execution.

Mitigation: Require explicit confirmation for each command and scope scanner execution to approved project directories.

Risk: The skill proposes writing security reports and may include sensitive vulnerability or secret-handling findings.

Mitigation: Choose report output locations before use and review generated reports before sharing them.

Risk: The optional callback_url parameter could send results to an untrusted destination.

Mitigation: Use callback URLs only for trusted endpoints and avoid sending security findings externally by default.

Risk: The artifact contains inconsistent API-key expectations.

Mitigation: Clarify which third-party scanners or API keys are required before invoking optional integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/security-hardening-shield)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports with checklists, findings, remediation examples, and inline shell commands or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose report files such as security-audit.md, vulnerabilities.md, remediation.md, and dependency-audit.md.]

## Skill Version(s):

1.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
