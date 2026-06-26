## Description: <br>
Place, list, and retrieve orders via the Zinc API (zinc.com). Use when the user wants to buy a product from an online retailer, check order status, list recent orders, or anything involving the Zinc e-commerce ordering API. Requires ZINC_API_KEY environment variable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a5huynh](https://clawhub.ai/user/a5huynh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent prepare and manage Zinc API checkout workflows, including creating orders, listing recent orders, and checking order status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real-money purchases through a configured Zinc account. <br>
Mitigation: Confirm every purchase, product, shipping address, and max_price with the user before sending POST /orders. <br>
Risk: Zinc API keys and checkout data, including shipping and order details, are sensitive. <br>
Mitigation: Install only when agent access to Zinc is intended, keep ZINC_API_KEY protected, and expect order and shipping details to be sent to Zinc. <br>


## Reference(s): <br>
- [Skill instructions](SKILL.md) <br>
- [Zinc API error reference](references/errors.md) <br>
- [Zinc API](https://api.zinc.com) <br>
- [Zinc API key signup](https://app.zinc.com) <br>
- [ClawHub release page](https://clawhub.ai/a5huynh/universal-checkout) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZINC_API_KEY and explicit user confirmation before creating orders.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
