## Description: <br>
Helps ecommerce teams estimate true per-order shipping costs across carrier, fulfillment, packaging, zone, and return assumptions for pricing and offer decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ecommerce operators, finance teams, and fulfillment analysts use this skill to model total delivery cost per order, compare carrier and zone scenarios, and choose shipping policies such as flat rate, threshold-based free shipping, pass-through pricing, or packaging changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business-sensitive shipping inputs may include carrier contracts, invoices, customer order exports, or zone distribution data. <br>
Mitigation: Use aggregated or redacted inputs unless sharing the underlying business data is approved for the analysis. <br>
Risk: Carrier rates, surcharges, and negotiated discounts may be stale or differ from current contracts. <br>
Mitigation: Verify rate assumptions against current carrier contracts, invoices, or approved rate tools before making pricing or policy decisions. <br>
Risk: Incomplete package, zone, fulfillment, or return assumptions can produce misleading margin guidance. <br>
Mitigation: Label each assumption with a confidence level and review the shipping checklist before relying on recommendations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leooooooow/shipping-cost-calculator-ecommerce) <br>
- [Carrier Rates & Surcharge Reference](references/carrier-rates-guide.md) <br>
- [Free-Shipping Threshold Strategy Playbook](references/free-shipping-playbook.md) <br>
- [Shipping Cost Output Template](references/output-template.md) <br>
- [Shipping Cost Model Quality Checklist](assets/shipping-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown with tables, calculations, assumptions, and decision recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes assumptions, per-order delivery cost breakdowns, zone segmentation, policy impact analysis, carrier comparisons when applicable, and risk flags.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
