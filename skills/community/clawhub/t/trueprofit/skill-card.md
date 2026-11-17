## Description:

TrueProfit profit analytics expert. Use this skill whenever working with TrueProfit MCP tools to analyze store performance, query profit data, orders, products, ad costs, or customer metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trueprofitdev](https://clawhub.ai/user/trueprofitdev)

### License/Terms of Use:


## Use Case:

External e-commerce merchants, Shopify operators, and agency users use this skill to query TrueProfit-connected stores for profit, revenue, order, product, advertising, shipping, and customer analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to replace the installed skill file with remote content returned by the TrueProfit MCP server.

Mitigation: Review updates through a trusted package or marketplace flow, inspect the diff, and verify provenance before replacing the installed skill file.

Risk: Using the skill requires connecting an authenticated TrueProfit account and exposing merchant analytics through MCP tools.

Mitigation: Install only for trusted stores and accounts, and confirm the user is comfortable using the connected TrueProfit data for analytics.

Risk: Profit analytics may be misleading when COGS is missing, ad platform data is delayed, currencies differ across shops, or UTM coverage is incomplete.

Mitigation: Surface the relevant caveat with results, avoid mixing currencies without confirmation and conversion, and warn when COGS or attribution gaps affect the answer.

## Reference(s):

- [TrueProfit ClawHub skill page](https://clawhub.ai/trueprofitdev/skills/trueprofit)
- [TrueProfit MCP server](https://mcp.trueprofit.io/mcp)
- [TrueProfit skill download](https://mcp.trueprofit.io/skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise analytics summaries, tables, tool-call guidance, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated TrueProfit MCP connection and shop context before querying merchant analytics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
