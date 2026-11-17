## Description:

Provides an authorization-first workflow for web security testing, guiding agents from scope checks through vulnerability assessment, audit trails, and structured reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Security practitioners and developers use this skill to plan and document web security assessments of targets they are authorized to test, including owned assets, approved bug-bounty scopes, CTFs, and local labs. It guides scope checks, vulnerability review, audit logging, and structured findings reports, with human review of conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scope checks may permit a target beyond the intended authorized path.

Mitigation: Independently confirm each authorized URL and its permitted paths; do not rely on the scope checker to enforce narrower path restrictions.

Risk: Credentials may remain in report metadata or audit logs despite redaction claims.

Mitigation: Remove credentials from inputs and manually inspect report metadata and audit logs before sharing.

Risk: External registry contents and live target behavior were not verified.

Mitigation: Use a reviewed local copy or verify the exact package version, choose the intended installation directory, and assess targets only after confirming their authorization.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/yottameta/skills/yotta-security-testing)
- [Project homepage](https://github.com/YottaMeta/yotta-security-testing)
- [Tutorial](references/tutorial.md)
- [Report template](references/report-template.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Shell commands]

**Output Format:** [Markdown guidance and Markdown or JSON assessment reports, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are based on supplied findings and need human review; the skill does not provide executable payloads.]

## Skill Version(s):

0.3.4 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
