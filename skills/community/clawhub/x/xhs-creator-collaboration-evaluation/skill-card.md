## Description:

根据用户提供的品牌、目标受众、预算和候选达人，比较小红书蒲公英报价、粉丝画像与内容表现，并整理合作适配度和待确认事项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

品牌团队和营销人员可用此技能评估自己提供的小红书达人候选名单。它整理报价、受众画像和内容表现，帮助比较预算适配度并标出数据缺口；结果不预测成交或投放回报。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly installs an unpinned CLI release, which could expose credentials or other available resources if the package or release is compromised.

Mitigation: Review the package and release before use, pin a specific reviewed version instead of using @latest, and keep the API key private and out of prompts and logs.

## Reference(s):

- [SocialDataX](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill listing](https://clawhub.ai/devinchen2014/skills/xhs-creator-collaboration-evaluation)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown comparison table with supporting notes and follow-up items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares only supplied candidates; distinguishes returned data from assessment and identifies data scope and missing information.]

## Skill Version(s):

1.0.7 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
