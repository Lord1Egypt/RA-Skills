## Description:

This skill collects and analyzes Amazon reviews through ARI to produce consumer insights, monitoring summaries, and seller recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

亚马逊卖家和市场研究人员可用此技能查看或采集 ASIN 评论，分析痛点、购买动因与趋势，并生成 VOC、竞品比较和 Listing 优化建议。

### Deployment Geography for Use:

ARI-supported Amazon marketplaces: US, UK, Germany, Japan, Canada, France, Spain, and Italy.

## Known Risks and Mitigations:

Risk: ARI credits may be charged before the user approves the price, including through a command documented as a free preview.

Mitigation: Set ARI to ask before every charge with autoconfirm off and verify the setting. Use quote for previews, approve recurring collection separately, and choose manual collection for a one-time run.

## Reference(s):

- [ARI CLI and API Reference](artifact/references/reference.md)
- [ARI Products](https://ari.funewa.com/zh/products)
- [ARI Reports](https://ari.funewa.com/zh/reports)
- [ARI Billing](https://ari.funewa.com/zh/billing)
- [ARI API Key Management](https://ari.funewa.com/zh/account?ui=d47626f#api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, HTML, JSON]

**Output Format:** [Natural-language insights and recommendations; Markdown or HTML reports, CSV review exports, and structured command results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings reflect ARI-collected review samples and may not cover all Amazon reviews.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata, frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
