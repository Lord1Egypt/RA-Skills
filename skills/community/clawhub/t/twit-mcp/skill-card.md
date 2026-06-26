## Description: <br>
Real-time X/Twitter data and write actions via x402 micropayments, including article, tweet, user, list, and community access plus posting, liking, reposting, bookmarking, and following actions paid per request in USDC on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etherlect](https://clawhub.ai/user/etherlect) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this MCP server to let an agent retrieve real-time X/Twitter content and perform authenticated account actions. The skill is intended for users who explicitly want per-request USDC payments from a configured Base wallet and controlled access to a connected Twitter/X account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend USDC from the configured Base wallet for each tool call. <br>
Mitigation: Use a dedicated low-balance wallet, keep approval enabled for paid actions, and avoid configuring a primary wallet. <br>
Risk: Authenticated Twitter/X write and delete actions can change a connected account. <br>
Mitigation: Connect only an account intended for agent use, approve write or delete actions explicitly, and disconnect the account after use. <br>
Risk: Twitter/X session cookies are stored locally and sent for authenticated actions. <br>
Mitigation: Use a trusted machine, protect the local credentials file, and revoke or disconnect the session when the skill is no longer needed. <br>


## Reference(s): <br>
- [twit.sh API reference and pricing](https://twit.sh) <br>
- [npm package: twit-mcp](https://www.npmjs.com/package/twit-mcp) <br>
- [x402 protocol documentation](https://x402.org) <br>
- [Base network](https://base.org) <br>
- [ClawHub skill page](https://clawhub.ai/etherlect/twit-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration] <br>
**Output Format:** [MCP tool responses as text or formatted JSON, with article content available as Markdown and setup guidance as configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, WALLET_PRIVATE_KEY for a funded low-balance Base wallet, and a connected Twitter/X account for write or delete actions.] <br>

## Skill Version(s): <br>
1.4.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
