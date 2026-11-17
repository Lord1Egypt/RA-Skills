## Description:

Use this skill to search Twitter/X for recent tweets matching keywords and engagement filters and return raw tweet data including text, author details, engagement counts, views, and URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berthelol](https://clawhub.ai/user/berthelol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and automation workflows use this skill to fetch recent Twitter/X posts for specified keywords, languages, lookback windows, and engagement thresholds. The skill returns raw tweet objects so the calling agent can decide whether and how to summarize, rank, or format the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Twitter/X API bearer token, and prompts or automation may expose sensitive search terms if confidential names, incidents, customer data, or secrets are used as keywords.

Mitigation: Provide the bearer token only in the configured environment variable and avoid confidential or secret search terms, especially in cron or automated agent workflows.

Risk: Twitter/X API calls can incur usage charges and consume rate or monthly read limits.

Mitigation: Set conservative max_results and lookback windows, fetch only the data needed, and monitor X API usage costs and caps.

## Reference(s):

- [Twitter API v2 Reference](references/twitter-api.md)
- [X Developer Platform](https://developer.x.com)
- [X Recent Search API Endpoint](https://api.x.com/2/tweets/search/recent)
- [ClawHub Skill Page](https://clawhub.ai/berthelol/skills/x-twitter-news-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON tweet objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned tweet objects include id, text, author, author_name, likes, retweets, replies, views, created_at, and url fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
