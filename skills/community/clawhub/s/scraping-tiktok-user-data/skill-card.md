## Description:

Scrapes TikTok user video history with per-video engagement metrics via apidojo's Apify TikTok User scraper for creator analysis, auditing, and benchmarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect TikTok creator video histories and engagement metrics for content analysis, auditing, and competitive benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can optionally collect complete follower or following lists, which may exceed the user's minimum necessary data needs.

Mitigation: Use only authorized TikTok data, keep follower and following collection disabled unless specifically justified, and set explicit collection limits.

Risk: The REST examples place APIFY_TOKEN in query URLs, which can expose credentials through logs, shell history, or shared links.

Mitigation: Prefer environment-based and header-based Apify authentication, and avoid logging or sharing token-bearing URLs.

Risk: The Apify actor uses pay-per-result pricing and may collect more results than expected when limits are omitted.

Mitigation: Set maxVideos, maxItems, or equivalent limits before execution and report the number of collected records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-tiktok-user-data)
- [Apify actor: apidojo/tiktok-user-scraper](https://apify.com/apidojo/tiktok-user-scraper)

## Skill Output:

**Output Type(s):** [markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown table with optional JSON or CSV files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN; optional Apify MCP; can save CSV or JSON when the runner script is available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
