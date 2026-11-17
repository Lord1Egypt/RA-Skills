## Description:

Researches topic trends across Hacker News, Reddit, GitHub, YouTube, and related platforms, then synthesizes actionable trend reports with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, analysts, and product teams use this skill to gather public trend signals from multiple platforms and turn them into concise market or topic research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic phrases such as 'what's trending' or 'market research' may activate the skill unexpectedly.

Mitigation: Install it only where broad trend-research triggers are acceptable, and review the invocation context before relying on the output.

Risk: Trend summaries from public web and API sources can reflect stale, incomplete, or misleading platform signals.

Mitigation: Verify cited sources and important claims before making business, research, or product decisions.

Risk: The default report template may use Chinese headings even when the surrounding workflow is in another language.

Mitigation: Specify the desired report language and heading style when invoking the skill.

## Reference(s):

- [Trend Harvester ClawHub skill page](https://clawhub.ai/aptratcn/skills/xiaobai-trend-harvester)
- [Hacker News Algolia search](https://hn.algolia.com/?q=AI+agent+skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown trend report with platform signals, source links, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include multilingual headings depending on the invocation and skill template.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
