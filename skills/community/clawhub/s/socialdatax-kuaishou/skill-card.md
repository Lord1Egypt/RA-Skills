## Description:

用于快手数据助手、快手内容研究、作品研究、作品详情、评论分析、评论回复分析、达人数据和达人作品。覆盖 Kuaishou / Kwai short-video research，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

外部用户可使用此技能查询快手 / Kwai 热榜、作品和达人信息，并分析作品评论及评论回复。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags repeated execution of an unpinned CLI that may change and access available credentials; the scan was partial and does not establish that the artifact is safe.

Mitigation: Review the CLI release before use, run it with only the required API credential in a restricted environment, and keep keys out of logs and generated files.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub release page](https://clawhub.ai/devinchen2014/skills/socialdatax-kuaishou)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Pretty-printed JSON results with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Kuaishou research results; no account actions]

## Skill Version(s):

0.1.25 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
