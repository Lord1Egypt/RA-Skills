## Description:

查询知了标讯的招投标公告、企业信息和市场数据，支持竞争对手分析与项目机会发现。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要招投标与采购情报的从业者，用于检索公告、了解企业投标记录和市场趋势，并发现拟建或临期项目。

### Deployment Geography for Use:

中国

## Known Risks and Mitigations:

Risk: Conflicting login-error instructions could trigger unintended device registration or account changes.

Mitigation: Resolve the re-registration instructions before use; for existing-key failures, follow user-directed recovery.

Risk: Searches reach Zhiliao, and hosted-service behavior and data retention were not verified.

Mitigation: Keep API keys and login links private, and avoid including sensitive information in searches.

Risk: Optional trial registration sends a stable device hash.

Mitigation: Use trial registration only with the user's consent; providing an API key normally skips device registration.

## Reference(s):

- [标讯搜索 API 说明](artifact/references/api-search.md)
- [企业分析 API 说明](artifact/references/api-company.md)
- [工商数据 API 说明](artifact/references/api-registry.md)
- [市场分析 API 说明](artifact/references/api-market.md)
- [账户查询 API 说明](artifact/references/api-account.md)
- [知了标讯技能发布页](https://clawhub.ai/zhiliaobiaoxun/skills/zhiliao-official-tender-assistant)
- [知了标讯 API](https://mcp-server.zhiliaobiaoxun.com/api_v2/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown text with concise summaries and tables where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results, company and market analysis, and project opportunity summaries based on requested queries.]

## Skill Version(s):

1.0.9 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
