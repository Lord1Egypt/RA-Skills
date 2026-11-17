## Description:

聚合并分析招投标数据，提供多维度统计、市场趋势、企业与品牌分析及历史中标价格查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

招投标从业者和市场分析人员可用此技能检索标讯、汇总地区或行业数据、比较采购方和中标方，并分析竞争格局与价格趋势。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and company names are sent to Zhiliaobiaoxun, and some successful queries may consume account credits.

Mitigation: Query only the data the user requests, explain applicable credit costs, and check the account balance when needed.

Risk: Optional automatic registration shares device features, including a hashed MAC address, to support trial-account deduplication.

Mitigation: Obtain the user's consent before registration; an existing API key skips this collection.

Risk: An exposed API key or temporary login link could allow access to the account.

Mitigation: Protect the saved API key and temporary login links, and share them only with their intended user.

## Reference(s):

- [标讯搜索 API 参数指南](artifact/references/api-search.md)
- [企业分析 API 参数指南](artifact/references/api-company.md)
- [市场分析 API 参数指南](artifact/references/api-market.md)
- [企业登记与资质 API 参数指南](artifact/references/api-registry.md)
- [账户查询 API 参数指南](artifact/references/api-account.md)
- [自动注册与隐私说明](artifact/references/auto-register.md)
- [提供方技能文档](https://ai.zhiliaobiaoxun.com/docs/skill)
- [ClawHub 技能页面](https://clawhub.ai/zhiliaobiaoxun/skills/tender-bid-union-zhongzhaolianhe)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results, rankings, aggregates, and trend summaries depend on the requested filters and returned provider data.]

## Skill Version(s):

1.0.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
