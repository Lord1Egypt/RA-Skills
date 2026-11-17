## Description:

热门标讯挖掘助手-火标网，当用户需要进行行业热度分析、统计Top采购商或聚合近期高频中标记录时调用，调用多维度聚合统计接口，呈现特定行业的市场热度与集中度趋势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users of procurement intelligence tools use this skill to analyze tender activity, identify leading purchasers and suppliers, and review company and market trends from bid records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic update acknowledgments use an endpoint whose authentication and ownership are not documented in the supplied evidence.

Mitigation: Ask the publisher to document and pin the authenticated confirmation endpoint before enabling automatic acknowledgments.

Risk: Search queries reveal users' procurement interests to the service provider.

Mitigation: Send only the terms needed for the requested analysis and avoid sensitive search terms.

Risk: Some company and market lookups consume account credits.

Mitigation: Use only the requested lookups, check the account balance, and review the applicable cost before making additional calls.

Risk: Temporary login links grant access to the associated account.

Mitigation: Share generated links only with the intended account holder and keep them out of public messages and logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/skills/trending-miner-huobiaowang)
- [Bid search API reference](artifact/references/api-search.md)
- [Company analysis API reference](artifact/references/api-company.md)
- [Market analysis API reference](artifact/references/api-market.md)
- [Company registry data guidance](artifact/references/api-registry.md)
- [Account API reference](artifact/references/api-account.md)
- [Account setup and login-link guidance](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Chinese-language text and Markdown summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results reflect the requested filters and available bid records.]

## Skill Version(s):

2.1.10 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
