## Description:

SKU对比分析 compares retail SKU performance across time periods, peer products, sales staff, sales metrics, and AIoT trial-to-conversion activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators and analysts use this skill to compare SKU sales, quantity, pricing, discount, inventory, AIoT conversion, and clerk performance across selected products and time periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded local import paths can load unreviewed local Python modules.

Mitigation: Package or pin dependencies and remove hard-coded external import paths before deployment.

Risk: The skill queries store, SKU, and clerk performance data.

Mitigation: Clearly disclose the data access, verify authorization, and validate and URL-encode API parameters.

Risk: An unused external skill import increases dependency surface.

Mitigation: Remove unused external imports or document why they are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-sku-comparison-analysis)
- [ClawHub publisher profile](https://clawhub.ai/user/gwyang7)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON-like Python dictionaries with printed analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns status, SKU or clerk identifiers, period metadata, change metrics, rankings, and generated insights.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
