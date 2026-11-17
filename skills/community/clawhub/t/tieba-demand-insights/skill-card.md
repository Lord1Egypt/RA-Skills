## Description:

当用户需要做百度贴吧用户需求研究、产品痛点归纳、购买顾虑整理或常见问题分析时，基于帖子与楼层讨论输出带原话依据的需求报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

产品团队、研究人员和内容策划者可用关键词、贴吧名称或帖子链接整理百度贴吧讨论中的需求主题、痛点、购买顾虑与常见问题，并查看帖子和楼层依据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes the SocialDataX CLI through npx using the mutable latest release, creating supply-chain and API credential exposure risk; scan coverage was partial.

Mitigation: Review and pin the CLI release before use, provide API credentials only in a trusted execution environment, and account for the scan's partial coverage when assessing the release.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/tieba-demand-insights)
- [SocialDataX API key and skill information](https://socialdatax.com/ai?from=clawhub)
- [SocialDataX billing](https://socialdatax.com/dashboard/billing)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown demand report with short quotations and post/comment references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes sample counts, observation scope, evidence strength, and known gaps when available.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
