## Description:

Fetch and analyze issues from Sentry error tracking. Use when asked to check Sentry errors, pull issues, investigate exceptions, review error trends, or get crash reports from a Sentry project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dave-b-b](https://clawhub.ai/user/dave-b-b)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect Sentry project issues, query unresolved errors, and retrieve issue details for troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sentry issue details and stack traces can expose sensitive project data.

Mitigation: Use the skill only where Sentry issue access is intended, avoid detailed output unless needed, and redact stack traces, breadcrumbs, tags, and context before sharing.

Risk: Authentication tokens can grant access to Sentry project data if overscoped or exposed.

Mitigation: Prefer SENTRY_AUTH_TOKEN over command-line token arguments and use a narrowly scoped read-only token.

## Reference(s):

- [Sentry API](https://sentry.io/api/0)
- [ClawHub Sentry Issues skill page](https://clawhub.ai/dave-b-b/skills/sentry-issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON issue output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Sentry issue metadata, stack traces, tags, breadcrumbs, and context when details are requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
