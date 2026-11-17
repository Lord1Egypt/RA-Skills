## Description:

Analyze Sentry error patterns, prioritize issues by user impact, identify root causes, and suggest targeted fixes. Use when asked to triage errors, analyze crash reports, or find the most impactful bugs to fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage Sentry issues, rank errors by user impact, identify likely root causes, and produce targeted fixes or prevention steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sentry exports and event payloads can contain secrets, personal data, or sensitive customer context.

Mitigation: Review and redact logs or event data before broad sharing, and limit analysis to data the agent is authorized to inspect.

Risk: Sentry API access requires an authentication token.

Mitigation: Use a least-privilege Sentry token scoped to the intended organization and project.

Risk: Root cause analysis and fix recommendations may be incomplete or incorrect without project-specific code and deployment context.

Mitigation: Have an engineer review recommendations against source code, release history, and reproduction evidence before applying changes.

## Reference(s):

- [Sentry project issues API endpoint](https://sentry.io/api/0/projects/{org}/{project}/issues/?query=is:unresolved&sort=freq&limit=50)
- [Sentry issue events API endpoint](https://sentry.io/api/0/issues/{issue_id}/events/?limit=10)
- [Sentry issue tags API endpoint](https://sentry.io/api/0/issues/{issue_id}/tags/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown report with inline shell commands and optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized issue summaries, impact scores, root cause analysis, fix recommendations, trend notes, and sprint planning guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
