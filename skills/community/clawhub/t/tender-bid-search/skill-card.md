## Description:

查询中国招投标公告、中标结果和采购意向，按关键词、地区、时间及金额初筛商机，并提供来源与筛选依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

采购与业务开发人员用它检索中国招投标信息、核查公告阶段和时效，并根据有来源的项目清单初筛跟进机会；结果不替代完整投标决策。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Bid queries, company names, API credentials and package identity are sent to the Zhiliaobiaoxun service; automatic registration may also send a hashed MAC-based device identifier.

Mitigation: Review what is sent to the service; configure ZLBX_API_KEY yourself before first use to avoid device-feature collection, and consent before automatic registration.

Risk: Broad searches and additional pages may consume paid platform credits.

Mitigation: Check costs and balance, limit search scope, and approve broader or bulk searches before they run.

Risk: Contact details and incomplete or stale bid records may be misused or mistaken for verified opportunities.

Mitigation: Avoid bulk use of contact data; retain source links and data gaps, and verify key dates and amounts before making bid decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bailianai/skills/tender-bid-search)
- [知了标讯平台](https://ai.zhiliaobiaoxun.com/)
- [标讯搜索接口说明](references/api-search.md)
- [商机分析接口说明](references/api-market.md)
- [账户与积分说明](references/api-account.md)
- [自动注册与隐私说明](references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown project lists and screening summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes search criteria, announcement sources, stage, dates, amounts, screening rationale, and missing-data caveats.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
