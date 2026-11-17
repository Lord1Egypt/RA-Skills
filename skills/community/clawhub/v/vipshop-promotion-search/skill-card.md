## Description:

查询唯品会（vip.com）当前或近期促销活动，并返回活动名称、时间、参与品牌、活动链接和活动图片等结构化信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[viphgta](https://clawhub.ai/user/viphgta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to check Vipshop promotion campaigns, group current and upcoming activities, and summarize brands, time windows, links, and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger login behavior and use local Vipshop account tokens.

Mitigation: Require explicit user approval before login, token use, or any account-linked request.

Risk: The skill may install or run a separate login skill.

Mitigation: Pin and verify the login dependency before installation or execution.

Risk: The skill covers broad shopping promotion intents that mention other platforms.

Mitigation: Limit activation to explicit Vipshop requests or clearly disclose when results are only for Vipshop promotions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/viphgta/skills/vipshop-promotion-search)
- [Vipshop promotion activity API](https://api.union.vip.com/vsp/common/getActListForAI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown summary with JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Vipshop login state; results depend on current activity data returned by Vipshop.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
