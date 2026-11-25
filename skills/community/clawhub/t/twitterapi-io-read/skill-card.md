## Description:

Read-only skill for twitterapi.io — look up public X/Twitter data (tweets, user profiles, followers and followings, advanced search, replies, quotes, trends, lists, communities) through the twitterapi.io REST API with a single x-api-key header. Use when the user wants to search, analyze or monitor public posts and accounts. Read-only: no posting, no account login, no credentials beyond the API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaitoinfra](https://clawhub.ai/user/kaitoinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to search, retrieve, monitor, and analyze public X/Twitter posts, profiles, followers, trends, lists, and communities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests and the API key are sent to the external twitterapi.io service, and API calls are billed.

Mitigation: Use only necessary public-data queries, keep the key in TWITTERAPI_IO_KEY without logging or committing it, and estimate call volume before long pagination or search jobs.

Risk: The security assessment was partial and recommends checking the external API destination.

Mitigation: Verify that twitterapi.io is the intended service before sending queries or using an API key.

## Reference(s):

- [twitterapi.io API documentation](https://docs.twitterapi.io)
- [twitterapi.io pricing](https://twitterapi.io/pricing)
- [twitterapi.io dashboard](https://twitterapi.io/dashboard)
- [X Developer Platform](https://developer.x.com)
- [twitterapi.io hosted MCP server](https://mcp.twitterapi.io/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Analysis, Shell commands, Code]

**Output Format:** [Public X/Twitter data returned as API responses, with text or Markdown summaries and optional shell or Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; API calls may incur per-call charges.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
