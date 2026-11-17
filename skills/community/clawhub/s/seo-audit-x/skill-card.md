## Description:

Provides comprehensive SEO audit and optimization for any website or URL, including on-page, technical, content, keyword, competitor, and reporting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[v3ads](https://clawhub.ai/user/v3ads)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and site operators use this skill to audit pages or domains, identify on-page and technical SEO gaps, compare competitors when provided, and produce actionable SEO reports and roadmaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional audit script can make unrestricted outbound requests to user-supplied URLs without private-address blocking or response-size limits.

Mitigation: Run only where outbound requests are sandboxed; add URL validation, redirect validation, private-address blocking, and response-size limits before enabling the script in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/v3ads/skills/seo-audit-x)
- [50-Point SEO Audit Checklist](references/checklist.md)
- [SEO Audit Report Template](references/report-template.md)
- [SEO Scoring Rubric](references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with optional JSON audit payload and inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional script accepts a target URL, competitor URLs, and keywords, then returns structured audit data for agent interpretation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
