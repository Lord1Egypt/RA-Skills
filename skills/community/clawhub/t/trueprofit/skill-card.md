## Description: <br>
Guides agents in using TrueProfit MCP tools to analyze Shopify store profit, revenue, orders, products, ad costs, shipping, COGS, ROAS, and customer metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trueprofitdev](https://clawhub.ai/user/trueprofitdev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External e-commerce merchants, analysts, and operators use this skill to query TrueProfit-connected Shopify performance data and choose the right MCP tools for profit, advertising, order, product, shipping, and customer analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide access to sensitive shop, order, product, advertising, and customer data through the intended TrueProfit MCP server. <br>
Mitigation: Use it only with the intended TrueProfit store, confirm the shop and date range before analysis, and avoid unnecessary customer-level lookups. <br>
Risk: COGS updates can affect all variants and retroactively change historical profit calculations. <br>
Mitigation: Require explicit user confirmation before COGS updates, especially bulk updates where variant_id is omitted or set to 0. <br>
Risk: Incomplete COGS, delayed ad attribution, refunds, or mixed shop currencies can make profit analysis misleading. <br>
Mitigation: Flag COGS gaps, recent ad reporting lag, refund spikes, and currency differences before presenting or comparing profit metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trueprofitdev/trueprofit) <br>
- [TrueProfit MCP server](https://mcp.trueprofit.io/mcp) <br>
- [TrueProfit skill download](https://mcp.trueprofit.io/skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with workflow steps, tool-selection tables, and concise analytics presentation advice.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to request confirmation for shop context, date ranges, sensitive customer lookups, and retroactive COGS updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
