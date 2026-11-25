## Description:

Send real best-selling flower bouquets with a card message to someone in Manhattan, New York (girlfriend, wife, partner, mom, grandma, sister, friend, host). Use when the user wants to surprise a loved one with flowers or a flower gift in Manhattan/NYC for a birthday, anniversary, apology, Thanksgiving, Hanukkah, Christmas, a bad week or just because. Five fixed all-in prices from $89 to $749; the user pays on a Stripe checkout link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rewoltor](https://clawhub.ai/user/rewoltor)

### License/Terms of Use:

MIT-0

## Use Case:

People sending a gift in Manhattan can use the skill to compare bouquet options, check delivery availability, prepare a card message, and place an order after confirming the full order details.

### Deployment Geography for Use:

Manhattan, New York (ZIP codes 10001–10282)

## Known Risks and Mitigations:

Risk: Placing an order sends recipient contact and delivery details, a card message, and buyer email to the Virag service; the security guidance advises considering whether the user is comfortable sharing these details.

Mitigation: Use only details the user provides, explain that the service receives them, read back the tier, price, recipient, address, date, and card text, and wait for a clear yes before creating the order.

## Reference(s):

- [Virag Flowers on ClawHub](https://clawhub.ai/rewoltor/skills/virag-flowers)
- [Virag service](https://virag-nine.vercel.app)
- [Remote MCP endpoint](https://virag-nine.vercel.app/mcp)
- [Flower card message guide](https://virag-nine.vercel.app/guides/what-to-write-on-a-flower-card)
- [Virag OpenAPI documentation](https://virag-nine.vercel.app/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Text, API calls, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides bouquet and delivery guidance and can prepare an order request; the skill requires clear user confirmation before creating an order. The target release is 1.0.0, while the artifact frontmatter reports 1.2.0.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
