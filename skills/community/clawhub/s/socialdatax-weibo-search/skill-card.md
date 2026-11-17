## Description:

Supports Weibo hot-search and post research for keyword discovery, content research, competitor analysis, and trend monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and content teams use this skill to review Weibo hot searches and posts, discover keyword signals, and study content, competitors, and trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium confidence and incomplete coverage, and its guidance flags broad activation wording and an unpinned npx reference for review.

Mitigation: Review the requested task and CLI command before execution, and check package references before running them.

Risk: The skill documents saving an API key for CLI use.

Mitigation: Keep SOCIALDATAX_API_KEY private and use the documented protected local credential storage; never include the key in outputs or logs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Concise text or Markdown summaries, with JSON data available from search calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps observed rankings and search results distinct from interpretation; includes IDs, URLs, authors, counts, and publish times when useful.]

## Skill Version(s):

0.1.25 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
