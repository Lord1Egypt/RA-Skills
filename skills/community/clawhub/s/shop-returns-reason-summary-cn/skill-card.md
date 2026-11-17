## Description:

将脱敏退款或退货原因和商品信息整理为可追溯的原因分类、按原始记录核算的计数与商品页改进建议，适合中文小店、小说作者和自媒体创作者复盘售后；缺少关键字段时明确列出缺口，不编造事实、不作财务结论或代替客服回复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

中文小店经营者、小说作者和自媒体创作者可用它复盘脱敏后的退款或退货记录，核对原因分类与商品计数，并整理可验证的商品页改进建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports reproduce supplied record fields, which could expose customer or order details.

Mitigation: Remove customer names, contact details, and identifying order information before supplying records.

Risk: Product-page recommendations could introduce inaccurate claims if applied without checking the underlying product details.

Mitigation: Verify each suggested change against the actual product and its specifications before updating the listing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xxjrq/skills/shop-returns-reason-summary-cn)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with traceable tables, summaries, and product-page recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves supplied record fields and separates reported facts from recommendations.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
