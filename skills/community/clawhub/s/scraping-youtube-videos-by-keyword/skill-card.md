## Description:

Scrapes YouTube videos matching keyword or search queries with apidojo's YouTube scraper on Apify and returns video metadata such as titles, channels, engagement counts, durations, and publish dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content researchers, SEO analysts, and market intelligence teams use this skill to collect YouTube search-result datasets and video-level metadata for a topic, keyword, URL, channel handle, or trend query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: REST examples place the Apify credential in URLs, which can expose the token through logs, screenshots, browser history, or command history.

Mitigation: Prefer the MCP or helper-script path when available, keep APIFY_TOKEN in a protected environment variable or secret manager, redact tokens from shared output, and rotate any token that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-youtube-videos-by-keyword)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, API Calls, Files]

**Output Format:** [Markdown with inline bash code blocks and tabular dataset output; saved outputs may be JSON or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN; results may include video identifiers, titles, channel metadata, engagement metrics, durations, URLs, thumbnails, descriptions, and publish dates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
