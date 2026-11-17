## Description:

Social media analytics and performance tracking. Track engagement, optimal posting times, competitor analysis, AI-powered insights, auto-generated charts, and weekly/monthly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content marketers, agencies, solopreneurs, and social media managers use this skill to review social account performance, compare competitors, identify posting windows, and generate actionable reporting from connected platforms or exported data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require social-platform credentials for full analytics.

Mitigation: Use read-only, least-privilege tokens where possible and keep credentials in the runtime environment rather than in prompts or shared files.

Risk: Generated reports can contain private business metrics, audience data, or competitor benchmarks.

Mitigation: Treat generated analytics and reports as confidential and review sharing permissions before distributing them.

Risk: Automatic reporting claims are not implemented by the inspected script.

Mitigation: Validate reporting behavior in the target runtime before relying on scheduled or delivered PNG/PDF reports.

Risk: Connecting social accounts increases exposure of account and engagement data.

Mitigation: Use manual CSV or exported-data mode when account connection is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly3094/skills/social-insights)
- [Publisher profile](https://clawhub.ai/user/fly3094)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal reports with tables, metrics, recommendations, and inline shell configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use social platform credentials when configured; can also operate from manually provided data or exported CSV files.]

## Skill Version(s):

1.3.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
