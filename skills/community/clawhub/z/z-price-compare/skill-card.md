## Description:

通过搜索引擎公开数据，比较各大电商平台商品价格，生成对比报告并提供个人购买建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhongzhiqiang-test](https://clawhub.ai/user/zhongzhiqiang-test)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for personal shopping research across Chinese e-commerce platforms, especially when they want a concise price comparison table and buying recommendation before checking the official product pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search-result prices, links, stock status, coupons, and member-only pricing may be stale or incomplete.

Mitigation: Treat the report as preliminary research and verify final prices and destination URLs directly on the official shopping platforms before buying.

Risk: The skill is not suitable for bulk commercial price monitoring or redistribution of platform-specific pricing data.

Mitigation: Use it for limited personal comparisons; commercial needs should use official platform or affiliate APIs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhongzhiqiang-test/skills/z-price-compare)
- [Platform Information Reference](artifact/references/platform_info.md)
- [Quick Start Guide](artifact/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown comparison reports with price tables, source links, caveats, and purchase recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices and links are preliminary search-result summaries and should be verified on official shopping platforms before purchase.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
