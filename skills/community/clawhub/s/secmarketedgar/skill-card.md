## Description:

Access SEC EDGAR-backed US company data, filings, metrics, ads, commerce tools, and research via a unified MCP API with audit-traceable lineage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afunsten](https://clawhub.ai/user/afunsten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and call SEC_Market MCP tools for US public-company research, SEC EDGAR-backed filings and metrics, product commerce, donations, delivery, and advertising workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment, donation, delivery, and advertising campaign tools can trigger high-impact actions.

Mitigation: Require explicit user confirmation before each call, including amounts, recipients, delivery targets, campaign content, and budgets.

Risk: Autonomous agents could invoke commerce or campaign operations without enough user-control scoping.

Mitigation: Review the skill before installation and restrict autonomous use of commerce, delivery, and ad-campaign tools unless policy controls are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/afunsten/skills/secmarketedgar)
- [SEC_Market MCP API Endpoint](https://market-royal-city.vercel.app/api/mcp)
- [SEC_Market MCP Discovery](https://market-royal-city.vercel.app/.well-known/mcp.json)
- [SEC_Market Agent Entrypoint](https://market-royal-city.vercel.app/.well-known/agent.json)
- [SEC_Market Product Catalog](https://market-royal-city.vercel.app/.well-known/agent-products.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks and MCP endpoint descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit-traceable lineage for company data where supported by the MCP API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
