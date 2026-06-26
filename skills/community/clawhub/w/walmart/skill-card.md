## Description: <br>
Plan Walmart grocery and household orders with pickup timing, substitutions, repeat restocks, and budget-aware cart decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to plan Walmart grocery and household restock workflows, including pickup or delivery timing, substitution rules, repeat baskets, order recovery, and pharmacy-adjacent operational planning with confirmation boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-assisted Walmart actions could change carts, checkout state, refills, cancellations, addresses, or substitutions before the user has reviewed them. <br>
Mitigation: Default to planning-only mode and require explicit user confirmation before checkout, refill, cancellation, address, or substitution changes. <br>
Risk: Local Walmart memory could capture sensitive credentials, payment data, insurance information, prescription identifiers, or medical details. <br>
Mitigation: Store only user-approved household planning notes in ~/walmart/ and exclude passwords, payment details, insurance identifiers, prescription identifiers, and medical history. <br>
Risk: Live prices, stock, pickup slots, delivery windows, and substitutions can change after a plan is drafted. <br>
Mitigation: Refresh live Walmart state before final actions and present timing, fulfillment, and substitution risks for user review. <br>
Risk: Pharmacy-adjacent workflows could be mistaken for medical advice or autonomous refill handling. <br>
Mitigation: Limit pharmacy support to operational planning, avoid dosage or interaction guidance, and require explicit confirmation before refill or pharmacy account workflows. <br>


## Reference(s): <br>
- [ClawHub Walmart Skill Page](https://clawhub.ai/ivangdavila/walmart) <br>
- [Walmart](https://www.walmart.com) <br>
- [Walmart Pharmacy](https://www.walmart.com/pharmacy) <br>
- [Walmart Marketplace Developer Documentation](https://developer.walmart.com/us-marketplace) <br>
- [Walmart Marketplace API Endpoint](https://marketplace.walmartapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with structured lists, tables, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Walmart planning notes under ~/walmart/ when the user approves.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
