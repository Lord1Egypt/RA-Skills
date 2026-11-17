## Description:

DeFi intelligence powered by Silverback — 19 x402 endpoints on Base chain. Market data, swap quotes, technical analysis, yield opportunities, token audits, whale tracking, and AI chat. Pay per call with USDC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ridingliquid](https://clawhub.ai/user/ridingliquid)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to query Silverback's paid DeFi intelligence endpoints for Base-chain market data, swap quotes, technical analysis, yield opportunities, token audits, whale tracking, and AI chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends DeFi queries and any supplied wallet addresses to Silverback's service.

Mitigation: Only use it when sharing those details with Silverback is acceptable.

Risk: Paid x402 calls may spend USDC from the agent's wallet.

Mitigation: Check pricing and endpoints first, use wallet spend limits, and review payment prompts before execution.

Risk: The optional MCP server is installed globally through npm.

Mitigation: Review or pin the package version before installing it in an agent environment.

## Reference(s):

- [Silverback DeFi Website](https://silverbackdefi.app)
- [Silverback x402 Documentation](https://silverbackdefi.app/x402)
- [Silverback x402 API](https://x402.silverbackdefi.app)
- [Silverback x402 MCP Package](https://www.npmjs.com/package/silverback-x402-mcp)
- [ClawHub Skill Page](https://clawhub.ai/ridingliquid/skills/silverback-defi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to make paid x402 API calls using USDC; free health, pricing, and endpoint checks are documented.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
