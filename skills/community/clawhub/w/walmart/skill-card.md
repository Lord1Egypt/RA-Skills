## Description:

Plan Walmart grocery and household orders with pickup timing, substitutions, repeat restocks, and budget-aware cart decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to plan Walmart grocery and household restocks, coordinate pickup or delivery timing, manage substitutions, and recover from order issues while keeping sensitive account, payment, and pharmacy details out of chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use an active Walmart account session for cart, checkout, order edits, cancellations, substitutions, or pharmacy workflows.

Mitigation: Keep planning-only mode unless the user explicitly approves browser-assisted action, refresh live price, stock, and slot state, and require explicit confirmation before any purchase or account change.

Risk: Local memory in ~/walmart/ can include household preferences and order history.

Mitigation: Store only approved planning notes and never store passwords, payment data, insurance identifiers, prescription numbers, or detailed medical information.

Risk: Pharmacy-adjacent tasks can be mistaken for medical advice.

Mitigation: Limit support to operational refill and pickup workflows, and direct medication, dosage, interaction, or side-effect questions to a pharmacist or clinician.

Risk: Inventory, prices, substitutions, and fulfillment windows are live conditions.

Mitigation: Recheck Walmart state before final recommendations or actions and flag split shipping, cold-chain, age-restricted, and sensitive substitution risks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/walmart)
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila)
- [Skill homepage](https://clawic.com/skills/walmart)
- [Walmart](https://www.walmart.com)
- [Walmart Pharmacy](https://www.walmart.com/pharmacy)
- [Walmart Marketplace Developer Portal](https://developer.walmart.com/us-marketplace)
- [Walmart Marketplace APIs](https://marketplace.walmartapis.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured basket lists, substitution rules, order-recovery steps, and optional local memory templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-confirmed browser workflow steps and local notes under ~/walmart/; no credentials, payment data, insurance identifiers, or prescription identifiers.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
