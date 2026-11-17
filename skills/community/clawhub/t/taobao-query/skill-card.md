## Description:

Query Taobao product prices and information through MCP (Model Context Protocol), including product search, price comparison, cart or order viewing, and seller chat while excluding payment operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evensix66](https://clawhub.ai/user/evensix66)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to search Taobao, compare prices for specific models or product categories, inspect cart/order information, and communicate with sellers through a configured Taobao MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access account-linked Taobao data and actions beyond price lookup, including cart changes, order/history reading, navigation, and seller chat.

Mitigation: Use only with a trusted local or TLS-protected MCP server and require explicit confirmation before reading orders/history, adding items to cart, navigating account pages, or sending seller messages.

Risk: A failed or untrusted MCP connection can produce unreliable operation status or expose account interactions.

Mitigation: Verify the Taobao desktop client and MCP endpoint before use, stop after repeated connection failures, and do not report product or account results unless the MCP call succeeds.

Risk: Payment, checkout, order confirmation, and financial authorization would create direct transaction risk.

Mitigation: Do not perform payment, checkout, order confirmation, or auto-buying operations; keep cart and browsing actions separate from purchase completion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evensix66/skills/taobao-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, links, troubleshooting text, and inline JSON or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Taobao/Tmall product links, price ranges, cart or order summaries, and MCP connection recovery guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
