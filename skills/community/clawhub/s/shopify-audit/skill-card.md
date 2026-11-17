## Description:

Audit Shopify store pages for conversion blockers including slow load, weak copy, missing trust signals, and friction in the add-to-cart flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Store owners, ecommerce operators, and conversion teams use this skill to audit Shopify storefronts across homepage, collection, product, cart, checkout, performance, and mobile flows. It produces a prioritized, executable fix list for conversion blockers such as weak copy, missing trust signals, surprise costs, slow pages, and add-to-cart friction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend Shopify payment, checkout, app, or theme changes that affect a live storefront.

Mitigation: Review suggested changes before applying them in production and validate important changes against baseline conversion, add-to-cart, and checkout metrics.

Risk: The audit can involve store URLs and conversion or checkout metrics that may be commercially sensitive.

Mitigation: Share only the store URL and metrics needed for the audit, and avoid including unnecessary private customer or order data.

## Reference(s):

- [Shopify Audit Skill Page](https://clawhub.ai/leooooooow/skills/shopify-audit)
- [Output Template](artifact/output-template.md)
- [Page-by-Page Guide](artifact/page-by-page-guide.md)
- [Trust and Performance Guide](artifact/trust-and-performance-guide.md)
- [Audit Quality Checklist](artifact/audit-quality-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown audit report with prioritized findings, scorecard, copy rewrites, performance summary, mobile notes, and re-audit schedule]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are capped at 15 and sorted by estimated revenue impact and implementation effort.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
