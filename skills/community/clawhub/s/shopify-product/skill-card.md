## Description:

Search Shopify products and analyze winning items with PPSPY. Filter products by price, category, sales, and revenue, and inspect bestselling products by store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce operators, and product researchers use this skill to search Shopify products, inspect category options, and review bestselling products by store through PPSPY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a globally installed npm MCP server and a PPSPY API key.

Mitigation: Install only if PPSPY and ppspy-mcp-server@1.0.1 are trusted, and run the server in an isolated or least-privilege environment.

Risk: PPSPY API calls can consume account credits and may incur usage costs.

Mitigation: Use a revocable PPSPY API key with spending limits where possible and monitor credit usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/shopify-product)
- [PPSPY homepage](https://www.ppspy.com)
- [PPSPY API site](https://api.ppspy.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries of Shopify product search results, categories, and bestselling products]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PPSPY API key; Shopify Product Search consumes 1 credit per record while supplement APIs are free.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter remains 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
