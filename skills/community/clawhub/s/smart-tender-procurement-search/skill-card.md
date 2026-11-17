## Description:

招标采购信息检索服务，按关键词、地区、金额、时间、行业等多维度检索全网招标公告与采购信息，支持高级逻辑（关键词分组、排除词）、获取标讯完整详情、查询临期周期性项目。当用户需要查招标公告、找采购信息、检索标讯、获取标书详情、跟踪某地区或行业项目动态时，必须使用此SKILL。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

招投标从业者、采购团队和供应商可按关键词、地区、金额、时间和行业检索中国招标采购公告，查看公告详情及项目进展，并查询企业和市场信息。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Optional registration sends a stable device fingerprint, and its retention and deletion terms are unspecified.

Mitigation: Review the registration privacy wording before installing; configuring your own API key bypasses device collection.

Risk: Search criteria are sent to Zhiliaobiaoxun, and successful queries may consume paid credits.

Mitigation: Send only the criteria needed for the requested lookup and check account balance or consumption when managing query costs.

Risk: The saved API key and generated login links could expose account access if shared or logged publicly.

Mitigation: Keep credentials and login links private and store the API key in a protected configuration.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhiliaobiaoxun/skills/smart-tender-procurement-search)
- [Search API reference](references/api-search.md)
- [Company API reference](references/api-company.md)
- [Market API reference](references/api-market.md)
- [Account API reference](references/api-account.md)
- [Registry data interpretation reference](references/api-registry.md)
- [Installation and skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Concise Chinese text summaries and Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include procurement notices, project timelines, company and market data, and account usage summaries.]

## Skill Version(s):

1.0.9 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
