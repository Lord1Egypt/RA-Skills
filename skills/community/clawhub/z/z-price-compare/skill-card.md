## Description: <br>
通过搜索引擎公开数据，比较各大电商平台商品价格，生成对比报告并提供个人购买建议。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zhongzhiqiang-test](https://clawhub.ai/user/zhongzhiqiang-test) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal shoppers use this skill to research prices for a small number of products across Chinese e-commerce platforms, then compare search-result snippets in a markdown report before verifying final purchase details on the platforms themselves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search-result prices, coupons, shipping, stock, and seller details may be incomplete or stale. <br>
Mitigation: Treat the report as initial research and verify final price, availability, seller trust, and platform terms directly before buying. <br>
Risk: Product names, budgets, and optional saved JSON reports can reveal shopping interests. <br>
Mitigation: Avoid sensitive purchase queries and handle saved reports as private files. <br>
Risk: The skill is not designed for purchases, account access, or commercial price monitoring. <br>
Mitigation: Use it only for limited personal research and rely on official platform or affiliate APIs for commercial workflows. <br>


## Reference(s): <br>
- [Platform Information Reference](artifact/references/platform_info.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhongzhiqiang-test/z-price-compare) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown comparison reports with tables, recommendations, and optional JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public search-result snippets for initial research; final prices and availability must be verified directly on each platform.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
