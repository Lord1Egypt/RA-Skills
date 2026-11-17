## Description:

Ralph Security Audit guides an agent through a comprehensive 100-iteration security audit covering OWASP Top 10, authentication, secrets, infrastructure, and code quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorukardahan](https://clawhub.ai/user/dorukardahan)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to perform structured security reviews of projects for weekly checks, new project onboarding, and pre-release audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect secrets and host or infrastructure details and write audit reports that may contain sensitive findings.

Mitigation: Scope the audit before use, instruct the agent not to print or save raw secrets, tokens, connection strings, private keys, cookies, or authorization headers, and review or delete .ralph-report.md after the audit.

## Reference(s):

- [Severity and Triage Reference](references/severity-guide.md)
- [ClawHub skill page](https://clawhub.ai/dorukardahan/skills/ralph-security)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit findings and reports with inline commands and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .ralph-report.md during an audit.]

## Skill Version(s):

3.0.0 (source: server release evidence; artifact metadata says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
