## Description:

查询浙江省招标与中标公告，并支持项目、企业及市场数据分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailianai](https://clawhub.ai/user/bailianai)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement and bidding teams use this skill to find tender and award notices, follow project stages, and review company or market data. Zhejiang is the default search region, while users can specify another region.

### Deployment Geography for Use:

China (Zhejiang by default; users may specify other regions)

## Known Risks and Mitigations:

Risk: Conflicting credential-recovery instructions could lead to account registration when an existing key fails.

Mitigation: Pause and repair or replace an existing key under the user's direction; do not trigger registration automatically.

Risk: Searches send company names and filters to Zhiliaobiaoxun and may spend credits. Optional trial registration sends device details and saves a local key.

Mitigation: Keep searches within the user's request, check credit use, obtain consent before optional trial registration, and keep saved keys and sign-in links private.

## Reference(s):

- [Tender search API reference](artifact/references/api-search.md)
- [Company data API reference](artifact/references/api-company.md)
- [Company registry interpretation guide](artifact/references/api-registry.md)
- [Market analysis API reference](artifact/references/api-market.md)
- [Account API reference](artifact/references/api-account.md)
- [Optional account registration guidance](artifact/references/auto-register.md)
- [Zhiliaobiaoxun service](https://ai.zhiliaobiaoxun.com/?ch=s152)
- [Zhiliaobiaoxun data API](https://mcp-server.zhiliaobiaoxun.com/api_v2/)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Concise text or Markdown summaries of retrieved bidding, company, and market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected search scope and provider data; some successful queries consume account credits.]

## Skill Version(s):

1.0.6 (source: artifact/SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
