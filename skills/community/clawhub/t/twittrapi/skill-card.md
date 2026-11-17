## Description:

Read public X (Twitter) data through the TwittrAPI REST API or its MCP server - user profiles, tweets, replies, followers, search with X operators, lists, communities and trends. Use when a task needs tweets, X accounts, follower lists, X search results or trending topics, or when writing code against api.twittrapi.com, or when the user wants a TwittrAPI account, API key or the MCP connector set up. Covers auth (X-API-KEY), the compact simple response format, cursor pagination, errors and retries, and keeping spend inside a budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twittrapi](https://clawhub.ai/user/twittrapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve public X data such as profiles, tweets, search results, followers, lists, communities, and trends through TwittrAPI. They can also configure access and manage pagination, retries, and prepaid-call spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a request that forwards an X session cookie.

Mitigation: Do not provide an X session cookie, and avoid installation until the session-cookie requirement has been removed.

Risk: The security review flags an unpinned package install command.

Mitigation: Review the package and version before installation.

Risk: The security review flags that an API key can be sent to a configurable destination.

Mitigation: Ensure the API key is sent only to a trusted HTTPS destination.

## Reference(s):

- [Endpoint reference](references/endpoints.md)
- [TwittrAPI full documentation](https://twittrapi.com/llms-full.txt)
- [TwittrAPI OpenAPI specification](https://twittrapi.com/openapi.json)
- [TwittrAPI pricing](https://twittrapi.com/pricing.json)
- [Hosted MCP setup guide](https://twittrapi.com/docs/hosted-mcp)

## Skill Output:

**Output Type(s):** [JSON data, Markdown summaries, Shell commands, Configuration guidance]

**Output Format:** [Structured API responses (JSON) and concise Markdown guidance or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public X data; paginated requests may require multiple billed calls.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
