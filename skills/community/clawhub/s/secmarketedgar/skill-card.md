## Description: <br>
Provides agents with SEC EDGAR-backed US company data, filings, metrics, advertising, commerce, and research through a unified MCP API with audit-traceable lineage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afunsten](https://clawhub.ai/user/afunsten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to discover SEC_Market MCP endpoints for US company research, SEC filing lookup, metrics with lineage, commerce, delivery, and advertising workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes purchase, donation, delivery, and advertising campaign creation tools through a remote MCP provider. <br>
Mitigation: Keep write, payment, delivery, and campaign tools behind explicit approval, spending limits, and review of prices, recipients, delivery details, and campaign parameters. <br>
Risk: The remote provider is outside NVIDIA control and must be trusted before use. <br>
Mitigation: Install and enable the skill only for trusted workspaces, and prefer read-only SEC research tools unless a user intentionally authorizes commercial actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afunsten/secmarketedgar) <br>
- [SEC_Market MCP endpoint](https://market-royal-city.vercel.app/api/mcp) <br>
- [MCP discovery document](https://market-royal-city.vercel.app/.well-known/mcp.json) <br>
- [Agent discovery document](https://market-royal-city.vercel.app/.well-known/agent.json) <br>
- [Agent products catalog](https://market-royal-city.vercel.app/.well-known/agent-products.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with endpoint lists and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP endpoint URLs and example curl requests; payment, delivery, donation, and ad campaign actions require explicit operator approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
