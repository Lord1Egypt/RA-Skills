## Description: <br>
Design a subscription or auto-replenishment program for consumable products including pricing tiers, frequency options, churn-reduction tactics, and the onboarding flow that maximizes trial-to-paid conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, ecommerce teams, and subscription program strategists use this skill to design subscribe-and-save or auto-replenishment programs for consumable products. It helps produce launch plans covering SKU selection, pricing, shipment cadence, onboarding, retention, win-back, dunning, and KPI targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated subscription plans may include pricing, cancellation, SMS/email, dunning, or legal-compliance decisions that are unsuitable for a specific business or jurisdiction. <br>
Mitigation: Use the output as planning support and require human review before deploying recommendations to customers. <br>
Risk: Prompts for subscription planning could include raw customer PII, payment details, credentials, or private analytics exports. <br>
Mitigation: Sanitize or aggregate sensitive data before use and omit credentials, payment details, and unnecessary customer identifiers. <br>
Risk: The skill can guide business decisions involving payment recovery and customer retention flows. <br>
Mitigation: Review dunning, cancellation, and win-back flows for customer experience, platform capability, and legal compliance before launch. <br>


## Reference(s): <br>
- [Output Template](references/output-template.md) <br>
- [Pricing Strategy Guide](references/pricing-strategy-guide.md) <br>
- [Churn Reduction Playbook](references/churn-reduction-playbook.md) <br>
- [Quality Checklist](assets/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown subscription program plan with tables, checklists, and recommended operating targets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include pricing tiers, frequency options, onboarding flows, churn-reduction tactics, win-back sequences, dunning guidance, and KPI targets.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
