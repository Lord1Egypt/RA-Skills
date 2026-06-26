## Description: <br>
OPC商城 helps agents query available OPC e-commerce products, reserve orders with recipient details, and read published product stories through documented public APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[legendaryfly](https://clawhub.ai/user/legendaryfly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and commerce agents use this skill to browse in-stock OPC products, place reservation orders after confirming recipient details, and read published product story content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order flows send recipient name, phone number, address, and order items to the documented OPC ordering service. <br>
Mitigation: Collect only the details needed for fulfillment, confirm them with the user before ordering, and use the skill only when the user trusts the service's privacy practices. <br>
Risk: Product availability, stock, order success, and story publication status can change at the service. <br>
Mitigation: Use the live API response as the source of truth and do not claim order success or story availability unless the service returns it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/legendaryfly/zhdf-shop-skills) <br>
- [Product search API](https://tools.gangzheng.tech/public/products/search) <br>
- [Order reservation API](https://tools.gangzheng.tech/public/orders/reserve) <br>
- [Published product stories list API](https://tools.gangzheng.tech/public/chronicles/list) <br>
- [Published product story detail API](https://tools.gangzheng.tech/public/chronicles/detail) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; API responses are treated as authoritative for product availability, order status, and published story content.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
