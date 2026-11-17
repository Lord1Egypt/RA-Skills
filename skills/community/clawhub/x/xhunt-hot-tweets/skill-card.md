## Description:

Extracts trending XHunt/X tweet rankings and returns tweet links, one-line Chinese summaries, engagement metrics, and short observations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dotheworknow](https://clawhub.ai/user/dotheworknow)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch XHunt trending tweet rankings for selected regions, time windows, and tags, then receive Chinese summaries with tweet links and engagement data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public XHunt pages and may return incomplete data if browser access or page extraction fails.

Mitigation: Prefer browser snapshot access where available, disclose fallback fetching when used, and mark missing fields as NA instead of inventing values.

Risk: Broad trigger examples may activate the skill for generic hot-post or trending-post requests.

Mitigation: Confirm or apply explicit region, time window, tag, result limit, and filtering mode before summarizing results.

Risk: Trending tweet summaries can include political or controversial content when the all mode is used.

Mitigation: Use the AI-product-only mode when the user requests product, model, or tooling updates and exclude unrelated political, crypto, entertainment, or empty content.

## Reference(s):

- [XHunt Trends](https://trends.xhunt.ai)
- [XHunt Hot Tweets on ClawHub](https://clawhub.ai/dotheworknow/skills/xhunt-hot-tweets)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with tweet links, one-line Chinese summaries, engagement metrics, and short observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses NA for missing data and notes degraded fetching or insufficient results when applicable.]

## Skill Version(s):

2.0.2 (source: server release metadata, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
