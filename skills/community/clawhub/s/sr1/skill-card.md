## Description:

Order food, groceries, and book restaurants in India via Swiggy's MCP servers with a safety-first confirmation workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aditya4206360-prog](https://clawhub.ai/user/aditya4206360-prog)

### License/Terms of Use:

MIT

## Use Case:

External users and their agents use this skill to search Swiggy food, grocery, and Dineout options in India, prepare carts or bookings, preview totals and locations, and proceed only after explicit user confirmation.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The skill can initiate real-world food, grocery, or restaurant booking actions through a Swiggy account.

Mitigation: Require a cart or booking preview with items, prices, total, location, and delivery or booking details before any order or booking command is run.

Risk: Security evidence reports a missing safety-enforcing CLI while the package declares a swiggy binary.

Mitigation: Review the installed package before use and do not rely on the CLI's documented safeguards unless the expected executable is present and verified.

Risk: Order logging may retain addresses, purchases, totals, and order IDs in local memory.

Mitigation: Treat order logs as sensitive data and restrict retention, sharing, and access to the minimum needed for user-requested follow-up.

Risk: Cash on Delivery orders cannot be cancelled once placed.

Mitigation: Confirm the user's final intent explicitly after showing payment method, address, item list, and total.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aditya4206360-prog/skills/sr1)
- [Swiggy MCP server manifest](https://github.com/Swiggy/swiggy-mcp-server-manifest)
- [Swiggy Food MCP endpoint](https://mcp.swiggy.com/food)
- [Swiggy Instamart MCP endpoint](https://mcp.swiggy.com/im)
- [Swiggy Dineout MCP endpoint](https://mcp.swiggy.com/dineout)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through Swiggy searches, cart or booking previews, confirmation prompts, and order logging.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact package.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
