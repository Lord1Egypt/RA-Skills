## Description:

Reduce per-shipment costs and improve delivery speed by analyzing carrier rates, package dimensions, zone distribution, and fulfillment method mix, with concrete rate negotiation targets and carrier selection rules for an order profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and logistics teams use this skill to audit shipment data, compare carrier and packaging options, and produce an optimization plan with carrier selection rules, surcharge reductions, and negotiation targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shipment invoices, customer ZIP distributions, carrier discounts, and shipping spend may contain business-sensitive information.

Mitigation: Provide only the minimum data needed for the analysis and avoid sharing unnecessary customer or contract details.

Risk: Carrier rates, surcharges, and service terms can change and may differ by account or contract.

Mitigation: Verify live carrier quotes and current contract terms before changing routing rules, fulfillment locations, or carrier agreements.

Risk: Packaging changes can reduce cost but may affect product protection or presentation.

Mitigation: Test revised packaging on a small shipment batch before committing it across the full catalog.

## Reference(s):

- [Output Template](artifact/output-template.md)
- [Carrier Rate Comparison Guide](artifact/carrier-rate-guide.md)
- [Packaging Optimization Guide](artifact/packaging-guide.md)
- [Quality Checklist](artifact/checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown plan with tables, checklists, and carrier selection rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided shipment, invoice, rate, zone, packaging, surcharge, and carrier contract data.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
