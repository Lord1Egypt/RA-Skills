## Description:

Full SEO audit and content brief generator for any website URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabierr](https://clawhub.ai/user/rabierr)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO practitioners use this skill to audit a website URL for technical SEO, on-page SEO, content quality, and keyword optimization, then generate an actionable Markdown report. When a target keyword is provided, it also produces a content brief with search intent, outline, metadata drafts, and internal linking suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unrestricted web requests from the agent environment to any user-supplied URL, including private network, localhost, or cloud metadata endpoints if the runtime permits it.

Mitigation: Review before installation and run only in environments where outbound web access is sandboxed to appropriate public websites.

Risk: Generated reports include a visible promotional footer.

Mitigation: Review report output before sharing it externally and confirm the footer is acceptable for the intended audience.

## Reference(s):

- [Report Template](references/report-template.md)
- [Content Brief Template](references/content-brief-template.md)
- [Scoring Rubric](references/scoring.md)
- [ClawHub Skill Page](https://clawhub.ai/rabierr/skills/seo-audit-pro-rabie)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with optional JSON audit data and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include score cards, prioritized recommendations, exact URLs, HTTP status codes, tag findings, file sizes, and an optional keyword-focused content brief.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
