## Description:

Look up recent sold prices / current market comps for any product via the 3rd Place Provisions sold-prices MCP endpoint (pay-per-call, x402, no API keys).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilnomie](https://clawhub.ai/user/lilnomie)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and reseller-focused agents use this skill to query product sale prices and current market comps through the sold_prices MCP tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The third-party MCP server receives product queries and logs each call.

Mitigation: Confirm product queries are appropriate to share with the third-party provider before use.

Risk: Paid x402 calls can charge $0.05 per paid call on capable clients.

Mitigation: Use client settings and budgets that make payment behavior visible before repeated or automated calls.

Risk: Results marked data_type "active" are asking-price comps rather than confirmed sale prices.

Mitigation: Check data_type, condition, and source before relying on a returned value.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilnomie/skills/sold-price-comps)
- [Publisher profile](https://clawhub.ai/user/lilnomie)
- [3rd Place Provisions Pulse](https://3rdplaceprovisions.com/pulse)
- [sold-price-comps MCP endpoint](https://api.3rdplaceprovisions.com/mcp)
- [x402 documentation](https://docs.x402.org)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON response returned as text, including query, provider, count, summary, data_type, comps, and disclaimer fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool accepts a product query and a limit from 1 to 10; active-listing results are asking-price comps, not confirmed sale prices.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
