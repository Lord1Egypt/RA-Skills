## Description:

OPC商城 helps agents query OPC/众合鼎富 products, place reservation orders through fixed public APIs, and read published product stories with curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legendaryfly](https://clawhub.ai/user/legendaryfly)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to browse in-stock OPC/众合鼎富 products, collect required order details, submit reservation orders, and retrieve published product story content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Placing an order sends phone number, recipient name, address, and selected item details to the OPC/众合鼎富 merchant endpoint.

Mitigation: Collect and confirm those details only when the user wants to order, disclose that they will be sent to the merchant service, and avoid ordering if the user is uncomfortable with that data sharing.

Risk: The skill depends on fixed external merchant APIs for product availability, story content, and order status.

Mitigation: Use only the returned API data, do not claim an order succeeded until the API confirms success, and surface stock or disambiguation errors to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legendaryfly/skills/zhdf-shop-skills)
- [OPC product search endpoint](https://tools.gangzheng.tech/public/products/search)
- [OPC order reservation endpoint](https://tools.gangzheng.tech/public/orders/reserve)
- [OPC published stories list endpoint](https://tools.gangzheng.tech/public/chronicles/list)
- [OPC published story detail endpoint](https://tools.gangzheng.tech/public/chronicles/detail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with inline curl commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Order flows may include phone number, recipient name, address, and selected item details in merchant API request bodies.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
