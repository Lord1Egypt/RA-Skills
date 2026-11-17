## Description:

云集会员制社交电商工具，提供自营+CPS双模式商品推荐、会员专属价查询和分销推广管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping assistants use this skill to answer Yunji price, member discount, rebate, and promotion-link questions for eligible products. It is intended to format product recommendation responses with item type, retail price, member price, and distribution commission details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping and commission-related recommendations may be invoked for broad shopping requests rather than explicit Yunji price, rebate, or promotion-link tasks.

Mitigation: Use tighter trigger wording or operator policy so the skill is invoked only for explicit Yunji price, rebate, member-price, or promotion-link requests.

Risk: Product prices, member discounts, promotions, and commission amounts can change over time.

Mitigation: Verify current pricing, discount, and commission details against an authoritative source before acting on or sharing recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/yunji)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured shopping rebate response containing product name, item type, retail price, member price, and distribution commission fields.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
