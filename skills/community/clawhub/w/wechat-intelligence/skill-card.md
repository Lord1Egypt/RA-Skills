## Description:

通过曼格云 API 增量监控多个公众号的新文章，辅助生成情报摘要、分析面板和数据导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

需要跟踪行业或竞品公众号的团队与个人，可用此技能采集新增文章、分析跨账号话题、制作每日简报，并导出本地分析结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API requests may incur unexpected charges.

Mitigation: Review the account list and live cost estimate, respect configured budgets, and obtain approval before exceeding them.

Risk: An API key or monitored article data could be exposed to an unintended service or local recipient.

Mitigation: Provide the key only through MANGYUN_API_KEY, keep the configured API endpoint trusted, and review the workspace and export destination.

Risk: Unverified article claims or embedded instructions could distort the analysis.

Mitigation: Treat articles as untrusted evidence, distinguish claims from verified facts, and check important conclusions against the linked originals.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dunkong/skills/wechat-intelligence)
- [曼格云 API 文档](https://api.we-media.cn/client/ai-guide)
- [曼格云 API 产品目录](https://api.we-media.cn/client/products)
- [分析结果导入规范](references/analysis-schema.md)
- [曼格云 API 调用规范](references/api-contract.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Shell commands, Configuration guidance, Files]

**Output Format:** [Chinese-language summaries and guidance; JSON analysis, local HTML dashboard, and XLSX workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source article links and reported API consumption for review.]

## Skill Version(s):

1.4.1 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
