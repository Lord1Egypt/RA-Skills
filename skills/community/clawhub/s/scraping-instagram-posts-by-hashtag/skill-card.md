## Description:

Scrapes Instagram posts for a hashtag through Apify and returns post URLs, captions, engagement counts, author handles, timestamps, and media metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, UGC collectors, and social media researchers use this skill to collect post-level Instagram hashtag datasets for trend analysis and content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: REST examples may place APIFY_TOKEN in URLs, which can expose credentials through logs, shell history, or shared command output.

Mitigation: Use header-based authentication such as an Authorization bearer token, keep APIFY_TOKEN in environment or secret storage, and avoid sharing logs that may contain request URLs.

Risk: Scraped Instagram outputs may contain social data such as user handles, captions, timestamps, media URLs, and engagement metrics.

Mitigation: Use the skill only for data you are allowed to collect, minimize the date range and maxItems scope, and protect exported CSV or JSON files.

Risk: Instagram restrictions, private accounts, rate limits, and banned hashtags can produce incomplete or zero-result datasets.

Mitigation: Set small maxItems limits, space repeated runs apart, document collection constraints, and validate outputs before using them for analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-instagram-posts-by-hashtag)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API call examples, and tabular dataset summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save Instagram hashtag results as CSV or JSON when the helper script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
