## Description:

Estimate ecommerce shipping cost per order across weight, zones, carrier rules, fulfillment costs, returns, and free-shipping policies so teams can make pricing, margin, and offer decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators, analysts, and developers use this skill to model true delivery cost per order and compare shipping policies, carrier options, free-shipping thresholds, and zone-level margin impact. It is intended for decision support where users can provide current carrier, fulfillment, packaging, return, and order-distribution inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Carrier-rate examples and surcharge ranges may be estimates or outdated.

Mitigation: Use current invoices, negotiated contracts, carrier quotes, or fulfillment-provider statements before making real-spend decisions.

Risk: Incomplete or assumed package, zone, return, or fulfillment inputs can produce misleading margin conclusions.

Mitigation: Label each input by source and confidence, calculate DIM weight, include fulfillment and return drag, and flag low-confidence assumptions in the output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leooooooow/skills/shipping-cost-calculator-ecommerce)
- [Structured Output Template](references/output-template.md)
- [Carrier Rates and Surcharge Reference](references/carrier-rates-guide.md)
- [Free-Shipping Threshold Strategy Playbook](references/free-shipping-playbook.md)
- [Shipping Cost Model Quality Checklist](assets/shipping-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown analysis with tables and calculation blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assumptions, delivery-cost stack, zone breakdown, policy scenarios, carrier comparisons, decision recommendations, and risk flags.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
