## Description:

Salai MCP (Beta) helps agents use Salai's remote MCP endpoint for Israeli grocery product search, cross-retailer price comparison, cart management, store and retailer discovery, and complementary recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idoziv](https://clawhub.ai/user/idoziv)

### License/Terms of Use:


## Use Case:

External users with approved Salai beta access use this skill to let an agent search Israeli grocery products, compare prices across retailers, manage carts, and request complementary recommendations through Salai MCP.

### Deployment Geography for Use:

Israel

## Known Risks and Mitigations:

Risk: The skill requires a Salai API key, which is a secret account credential.

Mitigation: Treat SALAI_API_KEY as a secret and never log or expose it in agent output.

Risk: Cart-management tools can add, update, remove, or delete items in a user's cart.

Mitigation: Ask the user to confirm before cart mutations, especially delete_cart and bulk updates.

Risk: Salai MCP is in beta and access may fail for users who are not approved.

Mitigation: If access is denied, instruct the user to complete beta signup and wait for approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/idoziv/skills/salai-mcp)
- [Salai App](https://app.salai.co.il)
- [Salai MCP Endpoint](https://mcp.salai.co.il/mcp)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [Markdown or plain text responses with MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SALAI_API_KEY; cart-management tools can mutate a user's Salai cart.]

## Skill Version(s):

0.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
