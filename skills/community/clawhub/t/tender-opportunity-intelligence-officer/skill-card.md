## Description:

帮助用户发现临期续约商机、分析竞争对手、定位潜在客户和供应商，并监控招投标动态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

销售、投标和市场情报团队可用它检索招投标公告、识别续约机会、分析企业及竞对，并梳理采购市场趋势。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches send company names and query criteria to Zhiliaobiaoxun and can consume account credits.

Mitigation: Use focused queries, check account balance and consumption when needed, and avoid fetching unrelated company data.

Risk: Optional trial registration may use a device hash, and the skill stores an API key and can return login links.

Mitigation: Use an existing API key when available, review and approve the registration consent prompt before proceeding, and keep saved credentials and generated links private.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/tender-opportunity-intelligence-officer)
- [招投标搜索 API 指南](references/api-search.md)
- [企业分析 API 指南](references/api-company.md)
- [市场分析 API 指南](references/api-market.md)
- [工商数据口径与解读边界](references/api-registry.md)
- [账户查询 API 指南](references/api-account.md)
- [API Key 自动注册与授权说明](references/auto-register.md)
- [知了标讯 Skill 文档](https://ai.zhiliaobiaoxun.com/docs/skill)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown summaries and result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the selected search criteria and available account credits.]

## Skill Version(s):

1.0.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
