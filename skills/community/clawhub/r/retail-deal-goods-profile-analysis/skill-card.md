## Description:

成交商品画像分析工具，用于分析成交商品的品类、价格带、颜色、包型、上市时间等特征分布及环比变化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators and analysts use this skill to review sold-product feature distributions and period-over-period changes for a selected store and date range. It supports category, price band, bag shape, color, launch-date, and summary finding analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads code from an unmanaged absolute local path outside the reviewed package before calling the BI API.

Mitigation: Package or pin api_client inside a trusted dependency path before use.

Risk: The skill queries store dashboard data by storeId and date range, which could expose retail performance data if used by an unauthorized user.

Mitigation: Verify the user is authorized for the requested storeId and date range before running the skill.

Risk: The generated report is Chinese-only.

Mitigation: Confirm Chinese-language output is acceptable for intended users or add localization before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-deal-goods-profile-analysis)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Plain text console report in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses store ID, date range, and optional store name inputs to print current and previous-period retail feature distributions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
