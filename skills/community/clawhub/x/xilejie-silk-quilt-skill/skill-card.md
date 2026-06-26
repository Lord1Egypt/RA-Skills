## Description: <br>
喜乐姐真蚕丝喜被 provides product consultation, buying guidance, silk authenticity and care information, purchase links, order intake, order lookup, and promotional updates for silk quilts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[malinguo](https://clawhub.ai/user/malinguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers use this skill to ask about 喜乐姐 silk quilt products, compare sizes and prices, get care and authenticity guidance, retrieve purchase links, and create cash-on-delivery orders after confirmation. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real cash-on-delivery orders. <br>
Mitigation: Require explicit user confirmation of product, quantity, price, phone number, and shipping address before calling the order tool. <br>
Risk: The merchant backend receives and stores customer delivery information. <br>
Mitigation: Publish privacy terms, retention and deletion instructions, and limit collected data to what is needed to fulfill the order. <br>
Risk: Order lookup can expose stored delivery details when queried by order number or phone number. <br>
Mitigation: Mask returned address data and require stronger verification before showing order details. <br>
Risk: Broad purchase-link triggers may promote buying before the user has clearly chosen a product. <br>
Mitigation: Use narrower purchase-link triggers and keep product, price, and order confirmation separate from casual product questions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/malinguo/xilejie-silk-quilt-skill) <br>
- [Publisher profile](https://clawhub.ai/user/malinguo) <br>
- [Gitee repository listed by artifact](https://gitee.com/lao-zou2026/xilejie-silk-quilt-skill) <br>
- [MCP endpoint listed by artifact](https://xilejie-silk.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Purchase links, Order confirmations] <br>
**Output Format:** [Natural-language responses with JSON tool results from MCP calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return product data, purchase links, order identifiers, and order status.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, skill.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
