## Description:

Fetch X/Twitter data via Apify actors. Search tweets, get user profiles, retrieve specific tweets with replies. Features local caching to save API costs. Works from any IP via Apify's proxy infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to search public X/Twitter posts, fetch user timelines, and retrieve tweet data through Apify actors with local caching to reduce repeat API usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend paid Apify credits and does not enforce a hard account-level spending cap.

Mitigation: Use an Apify account with spending limits, keep --max-results conservative, and monitor Apify billing.

Risk: URL mode can forward unintended X/Twitter URLs or query strings to Apify.

Mitigation: Pass only x.com or twitter.com tweet URLs and avoid URLs that contain secrets or sensitive query parameters.

Risk: Cached searches may store sensitive query context on disk.

Mitigation: Use --no-cache for sensitive searches or set X_APIFY_CACHE_DIR to a private cache directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/skills/x-apify)
- [Tweet Scraper V2 actor](https://apify.com/apidojo/tweet-scraper)
- [Apify pricing](https://apify.com/pricing)
- [Apify API token settings](https://console.apify.com/account/integrations)
- [Twitter advanced search query reference](https://github.com/igorbrigadir/twitter-advanced-search)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, configuration, files]

**Output Format:** [JSON by default, human-readable text summary on request, or saved output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized tweet records include id, text, author, author_name, created_at, likes, retweets, replies, and url.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
