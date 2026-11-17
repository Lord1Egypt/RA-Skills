## Description:

Search Shopify stores and products with PPSPY. Use this skill as a general Shopify library and Shopify spy tool for store, product, theme, and category research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Shopify stores, products, themes, traffic, categories, and bestselling products through PPSPY-powered search tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a globally installed third-party npm MCP server that receives the PPSPY API key.

Mitigation: Install only if PPSPY and ppspy-mcp-server@1.0.1 are trusted, use a revocable PPSPY API key, and prefer an isolated environment when global npm installs are a concern.

Risk: PPSPY API calls may consume account credits or affect billing.

Mitigation: Monitor PPSPY credit and billing usage, and manage or rotate the API key from the PPSPY API site.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/shopify-library)
- [PPSPY homepage](https://www.ppspy.com)
- [PPSPY API site](https://api.ppspy.com/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text responses with setup commands and Shopify research results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PPSPY_API_KEY and a globally installed ppspy-mcp-server npm package.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
