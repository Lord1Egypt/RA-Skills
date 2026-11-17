## Description:

为亚马逊卖家整理已订阅商品的待处理差评，生成买家沟通与申诉建议、产品改进方向，并跟踪处理状态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers use this skill to review collected customer feedback, prioritize negative reviews, and draft buyer replies, appeal suggestions, and product improvement ideas. It can also summarize review trends and track each review's handling status.

### Deployment Geography for Use:

Amazon marketplaces in the United States, United Kingdom, Germany, Japan, Canada, France, Spain, and Italy.

## Known Risks and Mitigations:

Risk: Analysis commands may spend ARI credits without a clear confirmation, including when a command appears to be a free preview.

Mitigation: Set and verify the account to ask before every charge with `autoconfirm off`, review the dedicated quote, and confirm the cost before analysis.

Risk: Recurring review collection and competitor monitoring can create ongoing credit costs.

Mitigation: Review the per-cycle price and schedule, and explicitly approve recurring collection or monitoring before enabling it.

Risk: The security guidance identifies unresolved billing behavior for `deepdive`.

Mitigation: Avoid `deepdive` until its billing behavior is fixed; use a dedicated quote flow for supported analysis instead.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/funewa/skills/review-reply)
- [ARI CLI and API reference](artifact/references/reference.md)
- [ARI monitoring center](https://ari.funewa.com/zh/monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV files]

**Output Format:** [Chinese natural-language responses and Markdown reports or reply suggestions; optional CSV, Markdown, or HTML exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the reviews collected for the selected Amazon marketplace; review samples may not cover every Amazon review.]

## Skill Version(s):

1.5.3 (source: server-resolved release, frontmatter, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
