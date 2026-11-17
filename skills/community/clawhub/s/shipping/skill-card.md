## Description:

Plan and manage parcel shipping decisions with carrier selection, landed-cost math, customs checks, and delivery exception playbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External shipping operators and ecommerce teams use this skill to plan parcel shipments, compare carrier options, estimate total landed cost, check customs readiness, and respond to delivery exceptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local shipping memory could contain customer-identifying details, tracking numbers, account data, or payment information if a user records them unnecessarily.

Mitigation: Store only reusable shipping preferences and operational patterns under ~/shipping/; redact sensitive identifiers and avoid storing payment credentials or account secrets.

Risk: Automatic activation for broad shipping or fulfillment mentions could surface shipping workflows in conversations where the user did not intend operational processing.

Mitigation: Confirm whether activation should apply to every shipping or fulfillment mention, only direct shipping requests, or only specific regions, carriers, or order types.

Risk: Carrier rates, surcharges, customs restrictions, and delivery status can change outside the skill's advisory files.

Mitigation: Verify current carrier quotes, documentation requirements, restricted item rules, and tracking events through authoritative carrier or customs sources before purchasing labels or committing to customers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/shipping)
- [Skill Homepage](https://clawic.com/skills/shipping)
- [Setup - Shipping Operations](setup.md)
- [Carrier Selection - Shipping Operations](carrier-selection.md)
- [International Customs - Shipping Operations](international-customs.md)
- [Exception Playbook - Shipping Operations](exception-playbook.md)
- [Memory Template - Shipping Operations](memory-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with checklists, tables, formulas, and local memory templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory workflow only; it does not buy labels, call carrier APIs, retrieve tracking events, or access shipping accounts by default.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
