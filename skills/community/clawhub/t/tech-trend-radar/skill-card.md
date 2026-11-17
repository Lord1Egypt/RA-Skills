## Description:

Use when generating current technology, AI model ranking, product, startup, funding, regulation, or market trend reports from recent industry updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chadlwm](https://clawhub.ai/user/chadlwm)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, and product teams use this skill to generate current technology and market trend reports across AI, developer tools, SaaS, cloud infrastructure, security, startups, funding, regulation, model rankings, and GitHub momentum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may perform fresh web research and produce reports that depend on the quality and recency of public sources.

Mitigation: Prefer primary sources, include publication dates or checked timestamps, cross-check major claims, and label uncertain signals as Watch.

Risk: The skill may create saved report or event files when invoked.

Mitigation: Review the generated report path and contents before sharing or relying on saved outputs.

Risk: Scheduled runs or downstream event-bus automation can generate recurring trend reports.

Mitigation: Enable recurring automation only when recurring reports are intended and review the schedule, scope, and recipients.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chadlwm/skills/tech-trend-radar)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown trend report with tables, dated evidence links, summaries, action items, watchlists, and optional saved report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may cover 1w, 1m, 3m, or explicit date ranges and may be saved under memory/research when the invoking agent supports file output.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
