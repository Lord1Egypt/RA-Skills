## Description:

Real-time X/Twitter data and write actions via x402 micropayments. Fetch articles, tweets, users, lists, and communities; post tweets, like, retweet, bookmark, follow; pay per request in USDC on Base. No API keys required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherlect](https://clawhub.ai/user/etherlect)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this MCP server to let an agent retrieve current X/Twitter articles, posts, users, lists, and communities, and to perform authenticated X/Twitter write actions when an account is connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server requires a funded wallet private key for x402 payments.

Mitigation: Use a dedicated low-balance wallet and avoid reusing a primary wallet key.

Risk: Connecting an X/Twitter account stores session cookies locally and enables account write actions.

Mitigation: Use a low-risk account, confirm write actions before use, and clear or revoke the session after use.

Risk: API_BASE can direct paid requests to a different remote service if overridden.

Mitigation: Keep the default API endpoint unless an override has been reviewed and is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/etherlect/skills/twit-mcp)
- [twit.sh API reference and pricing](https://twit.sh)
- [npm package: twit-mcp](https://www.npmjs.com/package/twit-mcp)
- [x402 protocol documentation](https://x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration]

**Output Format:** [MCP tool responses containing JSON-formatted text and Markdown article content; setup guidance uses shell commands and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some tool calls spend USDC from the configured Base wallet and write actions require a connected X/Twitter account.]

## Skill Version(s):

1.4.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
