## Description:

一个中文旅行积分奖励 skill，用于把用户当天的高能量行为转换成旅行积分，并反馈距离 50/100/300 分旅行目标的进度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyikoi](https://clawhub.ai/user/keyikoi)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to record daily high-energy actions, receive travel points, and see progress toward travel-themed reward tiers. It is not intended for booking, itinerary planning, visa advice, or general life coaching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad behavior matching may award travel points for vague user statements.

Mitigation: Review deployments for acceptable reward criteria and keep user-facing copy clear that approximate matching is intentional.

Risk: The skill can direct users to external preview pages that were not inspected as executable package code.

Mitigation: Validate linked pages separately before using them in a production or enterprise environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyikoi/skills/save-up-then-travel-clawhub)
- [Travel points web preview](https://save-up-then-travel-home.pages.dev/)
- [Product principles](artifact/references/product_principles.md)
- [Reward pool configuration](artifact/assets/reward_pool.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Chinese markdown with point totals, travel progress, and optional interaction links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses normally include behavior confirmation, earned points, accumulated travel progress, and a short emotional reinforcement.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
