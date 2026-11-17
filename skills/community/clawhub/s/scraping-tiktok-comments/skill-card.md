## Description:

Scrapes comments from any TikTok video using apidojo's TikTok Comments scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, brand monitors, content researchers, and developers use this skill to collect TikTok comment datasets from video URLs for sentiment analysis, community research, and product feedback extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: REST fallback examples place an Apify API token in URLs, which can expose credentials in logs or process history.

Mitigation: Prefer Apify MCP or a helper that keeps credentials out of URLs, use a dedicated least-privilege APIFY_TOKEN, and avoid command tracing or shared terminal logs.

Risk: Scraped TikTok comment datasets are third-party processed data.

Mitigation: Treat exported comments as third-party processed data and apply appropriate access controls and review before sharing or downstream analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-tiktok-comments)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and tabular TikTok comment datasets; optional CSV or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commenter usernames, comment text, like count, reply count, timestamps, reply nesting, and exported CSV/JSON datasets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
