## Description:

Scrapes TikTok profile statistics and metadata for lists of accounts using apidojo's TikTok Profile scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to collect TikTok account-level profile statistics for influencer vetting, data enrichment, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok account lists are sent to Apify for processing.

Mitigation: Use only account lists that are acceptable for third-party processing, and avoid sensitive or regulated datasets unless Apify processing has been approved.

Risk: Documented REST examples place the Apify token in request URLs.

Mitigation: Prefer Authorization-header authentication or environment-based tooling so tokens are not exposed in command history, logs, proxies, or shared URLs.

Risk: The customMapFunction option applies code-like transformation logic over scraped data.

Mitigation: Review custom mapping logic before use and keep it limited to expected, non-sensitive transformations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-tiktok-profile-data)
- [Apify TikTok Profile Scraper actor](https://apify.com/apidojo/tiktok-profile-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown with tables, inline shell commands, JSON examples, and optional CSV or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return username, nickname, follower count, following count, total likes, video count, bio, verification status, account privacy flags, profile links, and avatar URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
