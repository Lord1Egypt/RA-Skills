## Description:

Autonomous e-commerce storefront operations, store inventory curation, collectible valuations, and order fulfillment via Stockpile MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casualbrooks](https://clawhub.ai/user/casualbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and the agents they configure use Stockpile to manage storefront inventory, evaluate collectibles, handle store communications, monitor orders, and complete fulfillment. Consequential changes and credit use require user confirmation as described in the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package and Docker image are referenced without fixed versions, so installed code may change; the security scan also notes that credential and local access exposure should be considered.

Mitigation: Review setup before installing, prefer a reviewed fixed package version and fixed Docker image digest, and consider the API credentials and local access the server receives.

Risk: Inventory, routing, bulletin, credit, billing, and fulfillment actions can make consequential changes to storefronts, finances, or customer orders.

Mitigation: Follow the skill's confirmation boundaries: show the relevant item, destination, notice, credit use, plan details, or order and shipping details, then obtain explicit user confirmation immediately before the action.

## Reference(s):

- [Server-resolved source (GitHub)](https://github.com/casualbrooks/mcp-stockpile/tree/main/skills/stockpile)
- [Stockpile Market](https://stockpile.market)
- [Stockpile Agent Studio](https://stockpile.market/agents)
- [Stockpile merchant dashboard](https://stockpile.market/stores)
- [Stockpile agent API credentials](https://stockpile.market/agents/?tab=api)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration instructions]

**Output Format:** [Structured MCP requests and returned marketplace data, with Markdown setup guidance and concise summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change storefronts, spend credits, affect billing, or fulfill orders require explicit user confirmation as documented.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
