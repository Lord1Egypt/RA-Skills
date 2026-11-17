## Description:

上海迪士尼乐园游园助手，7项工具覆盖排队预估、路线规划、演出时间、餐厅推荐、门票价格，支持亲子/刺激/均衡多种路线风格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External visitors and travel-planning agents use this skill to plan Shanghai Disney Resort visits, estimate attraction waits, choose routes, check show and dining guidance, and review ticket and park-hour information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Park-hours lookup contacts a cloud proxy for Gaode data.

Mitigation: Install only when this network data flow is acceptable, and disclose that park-hours queries use the proxy.

Risk: Queue times, ticket prices, and attraction availability may be estimates or become stale.

Mitigation: Treat planning outputs as advisory and verify time-sensitive details in official Shanghai Disney channels before visiting or purchasing.

Risk: The artifact includes a fallback proxy token in code.

Mitigation: Rotate or remove embedded proxy credentials and use managed secrets for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/shanghai-disney)
- [Publisher profile](https://clawhub.ai/user/travel-skills)
- [Gaode proxy endpoint used for park-hours lookup](https://1439498936-bl10af74fl.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-like Chinese text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include estimated wait times, recommended routes, schedules, dining suggestions, ticket guidance, and caveats about non-real-time data.]

## Skill Version(s):

1.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
