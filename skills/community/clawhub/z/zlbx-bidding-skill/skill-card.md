## Description:

查询并分析招标、中标、企业、市场与采购数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

采购、投标与市场分析人员可用它查询招标和中标公告、企业与供应链信息，并整理采购趋势和品牌价格。它也可用于发现临期或拟建项目、比较竞争对手及潜在供应商。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional automatic signup uses a persistent device identifier, and the provider's retention and handling practices are unverified.

Mitigation: Prefer a manually obtained API key; before approving automatic signup, clarify how the provider retains and handles the device identifier.

Risk: Searches send company names, keywords, and filters to Zhiliaobiaoxun and may consume account credits; saved keys and generated login links could expose account access.

Mitigation: Use only the query details needed, protect the API key and login links, and review account consumption when using paid data calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liu-jiapeng/skills/zlbx-bidding-skill)
- [Publisher profile](https://clawhub.ai/user/liu-jiapeng)
- [知了标讯 skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Search API reference](artifact/references/api-search.md)
- [Company API reference](artifact/references/api-company.md)
- [Market API reference](artifact/references/api-market.md)
- [Registry API reference](artifact/references/api-registry.md)
- [Account API reference](artifact/references/api-account.md)
- [Automatic signup and key handling reference](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Text, Markdown]

**Output Format:** [Chinese text with summaries, lists, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on requested filters and account access; some data calls consume credits, and trial contact details may be masked.]

## Skill Version(s):

1.4.10 (source: artifact/SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
