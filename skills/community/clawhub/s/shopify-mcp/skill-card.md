## Description: <br>
Manage Shopify orders, customers, products, and inventory through a Python MCP server connected to the Shopify Admin REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzunglaviet](https://clawhub.ai/user/dzunglaviet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and interact with a Shopify MCP server so an agent can inspect and update store data such as orders, customers, products, inventory, and fulfillments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured MCP server can receive powerful Shopify Admin access that may change orders, fulfillments, customers, products, or inventory. <br>
Mitigation: Use a dedicated Shopify app with only the required scopes, start with read-only scopes where possible, and explicitly confirm the target store and action before any mutation. <br>
Risk: Shopify access tokens and multi-store credentials are sensitive and can expose store data or administrative actions if leaked. <br>
Mitigation: Keep environment files out of source control and rotate or revoke tokens if they are exposed or no longer needed. <br>
Risk: The setup depends on an external MCP server repository that is not included in this skill artifact. <br>
Mitigation: Review and pin the external repository before use, then re-check its behavior and dependencies before granting Shopify Admin access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dzunglaviet/shopify-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Shopify Admin credentials and an MCP server configured outside the skill artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
