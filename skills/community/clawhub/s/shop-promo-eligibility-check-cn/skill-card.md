## Description:

输入商家已确认的优惠有效期与时区、门槛口径、适用 SKU、叠加顺序及购物清单，输出逐条件可用、不可用或待确认表和可追溯计算步骤，适合客服与运营在活动前复核具体订单；缺少时间、运费口径或叠加授权时明确标为待确认，不猜平台规则或最优价。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

客服与运营人员用它根据商家确认的优惠规则核对具体购物清单，查看每项条件是否可用、不可用或待确认，并审阅逐步计算依据和规则明确时的应付草稿。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supplied stacking order can enable combined discount calculations even when merchant permission to combine the offers has not been confirmed.

Mitigation: Confirm that the merchant permits the combination before relying on the payable draft; keep missing authorization or terms marked as pending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxjrq/skills/shop-promo-eligibility-check-cn)
- [Saleor public discount-domain reference (business context only)](https://github.com/saleor/saleor)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON with condition results, traceable calculation steps, and a payable draft when supported by confirmed rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One known currency per request; supports up to 10 promotions and 20 cart lines. Missing or unconfirmed rules remain pending.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
