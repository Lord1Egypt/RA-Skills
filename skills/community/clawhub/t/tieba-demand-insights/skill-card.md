## Description:

基于关键词、贴吧名称或帖子链接，分析百度贴吧讨论中的用户需求、产品痛点、购买顾虑和常见问题，并提供原话依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

产品团队、市场研究人员和开发者可用此技能分析百度贴吧帖子及评论，归纳用户需求、痛点、购买顾虑和常见问题，并形成附原帖依据的报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安全审查指出，该技能会通过未固定版本的 CLI 包运行，可能使本地凭证面临供应链风险。

Mitigation: 使用前将 CLI 固定到已审查的版本并核验依赖；确认可以向 SocialDataX 发送搜索词和链接，避免提交机密信息。

Risk: 本次安全扫描未能解析部分本地引用，审查证据不完整。

Mitigation: 使用前检查未解析的引用及相关依赖。

## Reference(s):

- [SocialDataX 产品与 API Key 页面](https://socialdatax.com/ai?from=clawhub)
- [ClawHub 技能发布页](https://clawhub.ai/devinchen2014/skills/tieba-demand-insights)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [带帖子和评论引用的 Markdown 需求报告]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [注明样本量、观察范围、证据强弱、缺失信息和可尝试的后续行动。]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
