## Description:

Manage Shopify orders, customers, products, and inventory via natural language using the Shopify Admin REST API through a Python MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dzunglaviet](https://clawhub.ai/user/dzunglaviet)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators, support teams, and developers use this skill to connect an agent to a Shopify MCP server for order, customer, product, fulfillment, and inventory administration across one or more stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned third-party code with powerful Shopify credentials.

Mitigation: Use a pinned and audited shopify-mcp revision, lock dependencies, protect the Shopify token as a secret, and grant only the scopes needed.

Risk: The skill can support high-impact store changes such as order cancellation, fulfillment, customer updates, and inventory changes.

Mitigation: Require explicit confirmation before executing order cancellation, fulfillment, customer update, or inventory change actions.

## Reference(s):

- [Shopify MCP ClawHub listing](https://clawhub.ai/dzunglaviet/skills/shopify-mcp)
- [shopify-mcp repository](https://github.com/dzunglaviet/shopify-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Shopify Admin REST API actions through configured MCP tools.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
