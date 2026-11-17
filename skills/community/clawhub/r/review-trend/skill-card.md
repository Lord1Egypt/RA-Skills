## Description:

按时间追踪 Amazon 商品评论数量、评分与情绪走势，识别口碑转折并定位新增抱怨主题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and marketplace operators use this skill to monitor review volume, ratings, and sentiment for a product, spot reputation changes, and understand newly emerging customer complaints.

### Deployment Geography for Use:

Amazon marketplaces in the United States, United Kingdom, Germany, Japan, Canada, France, Spain, and Italy.

## Known Risks and Mitigations:

Risk: An analysis may spend account credits during a preview or after an unanswered quote.

Mitigation: Set confirmation to ask before every charge, use quotes for estimates, and leave unanswered quotes unapproved. Do not rely on deepdive as a free preview until that behavior is corrected.

Risk: Recurring review collection can create future account charges.

Mitigation: Approve recurring costs separately; use manual collection or pause monitoring when ongoing collection is not wanted.

## Reference(s):

- [ARI CLI and API reference](references/reference.md)
- [ARI monitoring center](https://ari.funewa.com/zh/monitor)
- [ARI product management](https://ari.funewa.com/zh/products)
- [ARI reports](https://ari.funewa.com/zh/reports)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, Guidance]

**Output Format:** [Chinese summaries and Markdown analysis reports; optional CSV review exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the selected ASIN, marketplace, collected reviews, and time range.]

## Skill Version(s):

1.5.3 (source: evidence.json release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
