## Description:

Scrapes TikTok videos for any hashtag or keyword using apidojo's TikTok scraper on Apify, returning video URLs, engagement metrics, author handles, captions, and timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, and social media teams use this skill to collect TikTok video datasets for hashtags, keywords, profiles, music pages, locations, challenges, or trends. It supports research and reporting workflows that need public TikTok metadata such as engagement counts, captions, author handles, video URLs, and timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok search inputs are sent to Apify, and results may include public author-identifying metadata.

Mitigation: Use the skill only when that data flow is acceptable, avoid unnecessary retention or redistribution of author-identifying data, and follow the security guidance in the release evidence.

Risk: Apify token handling can expose credentials if tokens are placed directly in URLs or copied into logs.

Mitigation: Prefer the MCP or helper-script workflow, keep APIFY_TOKEN in environment-based configuration, and use Authorization headers rather than URL tokens when calling APIs directly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-tiktok-videos-by-hashtag)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, JSON examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to save TikTok metadata as CSV or JSON when requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
