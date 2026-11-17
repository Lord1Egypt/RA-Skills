## Description:

Scrapes tweets matching any keyword, hashtag, phrase, or boolean query using apidojo's Twitter Search scraper on Apify and returns tweet text, author, engagement counts, timestamp, and tweet URL for downstream analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, data analysts, journalists, and social listening teams use this skill to collect tweet datasets for keyword, hashtag, phrase, account, mention, location, engagement, language, and date-filtered searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tweet search terms, filters, and resulting datasets are sent to Apify and may expose sensitive or confidential research intent.

Mitigation: Avoid sensitive searches and review organizational data handling requirements before running collection jobs.

Risk: Documented REST examples place the Apify API token in query strings, which can leak through shell history, logs, or proxies.

Mitigation: Prefer Authorization headers, MCP-based token handling, or a least-privilege Apify token rather than query-string token usage.

Risk: Broad external scraping options can collect large or policy-sensitive datasets.

Mitigation: Limit `maxItems`, narrow date ranges, deduplicate results, and review collected data before sharing or storing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/scraping-tweets-by-keyword)
- [Apify tweet scraper actor](https://apify.com/apidojo/tweet-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or CSV tweet dataset outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tweet datasets include fields such as id, text, author identifiers, engagement counts, language, timestamp, tweet URL, media, retweet and quote flags, and source.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
