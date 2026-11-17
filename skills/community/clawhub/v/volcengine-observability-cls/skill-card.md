## Description:

Log query and troubleshooting workflows with Volcengine CLS. Use when users need error analysis, time-range queries, aggregation dashboards, or incident diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to investigate Volcengine CLS logs, build time-range and aggregation queries, summarize affected services and error counts, and identify concrete remediation steps during incidents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLS log investigations may expose secrets or personal data if sensitive log content is shared unnecessarily.

Mitigation: Confirm the intended Volcengine CLS use case and redact secrets or unnecessary personal data before providing logs to the agent.

Risk: Runtime access depends on the external tools and credentials provided by the user.

Mitigation: Grant only the minimum credentials and tool permissions needed for the specific investigation.

## Reference(s):

- [Sources](references/sources.md)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/volcengine-observability-cls)
- [Publisher profile](https://clawhub.ai/user/cinience)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with CLS query statements, affected services, counts, findings, and remediation suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable query templates for follow-up investigations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
