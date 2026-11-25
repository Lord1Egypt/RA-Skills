## Description:

Research crypto tokens, tracked traders, wallets, and smart-money activity using StalkChain's connected MCP tools. Use for StalkChain setup or requests about on-chain holdings, trader PnL, token holders, buy/sell flow, and token risk. This skill does not place trades or manage funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[assistant-design](https://clawhub.ai/user/assistant-design)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect to StalkChain when needed and research token activity, trader portfolios, wallet holdings, smart-money flows, and token risk using connected service data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research requests are sent to StalkChain's hosted service, and connecting may require sign-in and approval.

Mitigation: Confirm you trust StalkChain before connecting and review its sign-in prompts; do not share seed phrases or private keys.

Risk: Research lookups can spend StalkChain credits, and service coverage varies by tool and chain.

Mitigation: Check pricing and returned usage, agree on paid calls before running them, and report the chain, time window, freshness, and any unavailable or limited results.

## Reference(s):

- [StalkChain documentation](https://stalkchain.com/docs)
- [OpenClaw setup guide](https://stalkchain.com/ai/openclaw)
- [StalkChain MCP directory](https://data.stalkchain.com/mcp/directory)
- [Machine-readable service guide](https://data.stalkchain.com/llms.txt)
- [Pricing and credit information](https://stalkchain.com/pricing)
- [StalkChain plugin repository](https://github.com/StalkC/stalkchain-plugin)
- [StalkChain support](https://stalkchain.com/support)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown research summaries and setup guidance, with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research may include chain, address or handle, time window, source timestamp, data freshness, uncertainty, and returned credit usage.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
