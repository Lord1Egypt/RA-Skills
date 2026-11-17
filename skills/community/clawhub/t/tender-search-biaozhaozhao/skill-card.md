## Description:

招投标快捷检索引擎-标找找，当用户需要快速查询特定关键词的招标或中标公告时调用，优先调用基础搜索工具提取项目名称、金额和链接，输出精简直接的列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要查询中国招标、中标公告或分析企业与采购市场的用户，按需检索项目、企业和市场数据，并整理成简明结果。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Update acknowledgments may send the API key without clearly limiting the destination.

Mitigation: Before installing or updating, verify the acknowledgment destination and approve only the expected provider endpoint; do not send a key when the destination cannot be validated.

Risk: Automatic registration can use a MAC hash to recognize a device, and searches send criteria to the provider; server-side behavior and data retention were not verified.

Mitigation: Use a personally supplied API key to avoid device fingerprinting, send only necessary search criteria, and protect stored keys and generated login links.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liu-jiapeng/skills/tender-search-biaozhaozhao)
- [Bid search API reference](artifact/references/api-search.md)
- [Company analysis API reference](artifact/references/api-company.md)
- [Company registry query guidance](artifact/references/api-registry.md)
- [Market analysis API reference](artifact/references/api-market.md)
- [Account query API reference](artifact/references/api-account.md)
- [Automatic registration guidance](artifact/references/auto-register.md)
- [Tender data API endpoint](https://mcp-server.zhiliaobiaoxun.com/api_v2/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Concise Markdown lists and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project titles, amounts, links, search criteria, and company or market data; some successful queries consume account credits.]

## Skill Version(s):

1.0.10 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
