## Description:

Get public Facebook and Instagram data (pages, posts, comments, groups, photo albums, Meta Ads Library, Marketplace listings, Instagram profiles, posts, reels and locations) through the SocialAPIs REST API or its MCP server. Use when the user wants to look up, monitor, compare or analyze public Facebook or Instagram content, competitors' ads, or Marketplace listings, or wants code that does.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oussemafr](https://clawhub.ai/user/oussemafr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to retrieve and review public Facebook and Instagram pages, posts, groups, ads, Marketplace listings, profiles, reels, and locations through SocialAPIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed API key could allow unauthorized use of the SocialAPIs account.

Mitigation: Read SOCIALAPIS_API_KEY from the environment; never paste it into chat, hard-code it, print it, or put it in a URL.

Risk: Lookup queries are sent to SocialAPIs, and API calls consume account credits.

Mitigation: Use only the queries needed for the task and check usage and likely credit costs before large batches.

Risk: Public social data can still be misused to track or profile private individuals or to spam people.

Mitigation: Use the skill only for lawful, responsible purposes; do not use it to track or profile private individuals or to spam people.

Risk: Installing the optional local MCP package introduces a package supply-chain risk.

Mitigation: Pin a reviewed package version when using the local MCP server; REST and hosted MCP are also available.

## Reference(s):

- [SocialAPIs endpoint reference](references/endpoints.md)
- [SocialAPIs OpenAPI specification](https://socialapis.io/openapi.json)
- [SocialAPIs hosted MCP server](https://mcp.socialapis.io/mcp)
- [SocialAPIs ClawHub release](https://clawhub.ai/oussemafr/skills/socialapis)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Code, API Calls]

**Output Format:** [Markdown guidance, API calls, JSON results, and optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Facebook and Instagram data; API calls require a SocialAPIs key and consume account credits.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
