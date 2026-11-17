## Description:

MCP Tools skill for AI agent commerce. Use when a user wants agentic Shopping to search/compare products, prepare a buyer-confirmed cart, and create a merchant-hosted checkout handoff link, or when an agent needs to register/reuse a hosted UCP identity (agent_id). Provider-neutral UCP Shopping MCP tools; no scraping and no payment handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theagenttimes](https://clawhub.ai/user/theagenttimes)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let agents search and compare products, manage buyer-confirmed carts, and create merchant-hosted checkout handoff links while reusing a hosted UCP identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can send shopping or checkout details to a gateway URL supplied through the environment.

Mitigation: Keep UCP_GATEWAY_MCP_URL unset or set only to a trusted HTTPS endpoint before using helper scripts or live MCP calls.

Risk: Cart and checkout actions can affect a buyer's shopping session.

Mitigation: Require explicit buyer or operator confirmation before cart create, update, cancel, or checkout handoff actions.

Risk: Payment details could be exposed if entered into the agent workflow.

Mitigation: Enter payment details only on the merchant-hosted checkout page and do not provide card, bank, wallet, token, password, or payment-code fields to the agent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theagenttimes/skills/ucp-gateway-skill)
- [UCP Gateway Homepage](https://ucpg.ai/)
- [UCP Gateway MCP Endpoint](https://ucpg.ai/mcp)
- [UCP Gateway Registry](https://ucpg.ai/registry)
- [Source Repository](https://github.com/theagenttimes/ucp-gateway-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and MCP tool names.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to call external UCP Gateway MCP tools for product search, cart operations, checkout handoff, profile registration, and profile lookup.]

## Skill Version(s):

0.2.4 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
