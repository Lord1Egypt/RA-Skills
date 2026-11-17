## Description:

Optimize product color, size, and variant offerings based on sales data, market trends, and inventory constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators use this skill to analyze variant-level sales, return, margin, trend, competitor, and inventory data and produce specific Keep, Promote, Retire, Add, or Test recommendations for product variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide product-level business metrics and can produce recommendations that affect inventory, pricing, promotions, or variant retirements.

Mitigation: Review recommended retirements, promotions, test quantities, and inventory changes with the responsible business owner before acting.

Risk: Recommendations may be weak when variant-level sales, margin, return, inventory, audience, platform, seasonal, or competitor data is incomplete.

Mitigation: Provide the required data points listed by the artifact and treat unsupported recommendations as hypotheses for validation.

Risk: Trend, seasonal, size-curve, and competitor benchmarks may not match a specific brand, region, audience, or channel.

Mitigation: Validate benchmark-based advice against the user's own demand signals, return reasons, and sell-through history before purchasing or retiring inventory.

## Reference(s):

- [Output Template](references/output-template.md)
- [Color Trend & Selection Guide](references/color-trend-guide.md)
- [Size Curve Reference Guide](references/size-curve-reference.md)
- [Variant Strategy Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report with tables, recommendations, implementation phases, and monitoring specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided product, platform, audience, sales, margin, return, inventory, seasonal, and competitor context for best results.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
