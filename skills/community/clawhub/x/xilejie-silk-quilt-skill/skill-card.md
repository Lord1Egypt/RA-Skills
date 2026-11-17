## Description:

喜乐姐真蚕丝喜被的产品咨询与下单服务，支持查询品牌故事、产品规格价格、选购推荐、蚕丝真伪鉴别、洗涤保养、售后政策、下单留言、最新活动和货到付款。

This skill is ready for commercial/non-commercial use.

## Publisher:

[malinguo](https://clawhub.ai/user/malinguo)

### License/Terms of Use:

MIT

## Use Case:

External shoppers use this skill to ask about 喜乐姐 silk quilts, compare sizes and prices, get care and authenticity guidance, obtain purchase links, and create cash-on-delivery order requests after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real orders and handle customer names, phone numbers, and addresses.

Mitigation: Require explicit user confirmation before order creation and deploy only with authentication, authorization, rate limiting, address masking, and a clear privacy notice.

Risk: Order lookup can expose customer address data if access is not controlled.

Mitigation: Require phone verification or equivalent authorization for order lookup and avoid returning full addresses unless necessary.

Risk: The bundled backend depends on unpinned package ranges.

Mitigation: Pin and review backend dependencies before public deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/malinguo/skills/xilejie-silk-quilt-skill)
- [Source Repository](https://gitee.com/lao-zou2026/xilejie-silk-quilt-skill)
- [MCP Service Endpoint](https://xilejie-silk.com)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Natural-language responses supported by MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product recommendations, purchase links, order confirmations, and order status details.]

## Skill Version(s):

0.1.0 (source: frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
