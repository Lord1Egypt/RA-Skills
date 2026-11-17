## Description:

Use TweetAPI or its hosted MCP server for read-only public Twitter/X data. Use for public profile, tweet, search, list, community, space, relationship, and documentation lookups, or to add server-side TweetAPI reads to an application. Do not use for posting, engagement, account access, private messages, login automation, billing, or administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[restocked](https://clawhub.ai/user/restocked)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve public Twitter/X data and documentation through TweetAPI, or to integrate read-only, server-side lookups into an application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup requests are sent to a third-party service and consume API quota.

Mitigation: Review TweetAPI's privacy policy, approve only read-only MCP access, and tell the user before spending quota.

Risk: Misuse or exposure of credentials could compromise accounts or applications.

Mitigation: Keep application API keys server-side; never provide Twitter/X passwords, cookies, or session tokens.

## Reference(s):

- [TweetAPI skill release](https://clawhub.ai/restocked/skills/tweetapi)
- [TweetAPI Agent Integration Guide](https://tweetapi.com/docs/getting-started/agents)
- [TweetAPI OpenAPI Specification](https://tweetapi.com/openapi-v2.json)
- [Hosted MCP setup guide](references/hosted-mcp.md)
- [Application integration guide](references/integration.md)
- [Current public sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls, Code, Configuration]

**Output Format:** [Text or Markdown, including public lookup data and code or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public lookups; live requests consume quota and default to one result page.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
