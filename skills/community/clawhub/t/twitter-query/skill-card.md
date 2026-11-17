## Description:

Query X/Twitter via twitterapi.io read-only APIs by account user timeline or by keyword advanced search, producing structured JSON without bundled LLM summarization or trend scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexander10011](https://clawhub.ai/user/alexander10011)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch read-only X/Twitter user timelines or advanced keyword search results via twitterapi.io for downstream analysis or summarization in the current conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send TWITTER_API_KEY, usernames, and search queries to an arbitrary API base if TWITTER_API_BASE is set.

Mitigation: Use only in a trusted environment, leave TWITTER_API_BASE unset or set it exactly to https://api.twitterapi.io, and treat the API key, usernames, and queries as outbound data.

## Reference(s):

- [twitterapi.io Documentation](https://docs.twitterapi.io/introduction)
- [twitterapi.io User Last Tweets Endpoint](https://docs.twitterapi.io/api-reference/endpoint/get_user_last_tweets)
- [twitterapi.io Advanced Search Endpoint](https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search)
- [Twitter Advanced Search Syntax Reference](https://github.com/igorbrigadir/twitter-advanced-search)

## Skill Output:

**Output Type(s):** [JSON, shell commands, configuration, guidance]

**Output Format:** [JSON printed to stdout with concise Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TWITTER_API_KEY; optional TWITTER_API_BASE defaults to https://api.twitterapi.io.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
