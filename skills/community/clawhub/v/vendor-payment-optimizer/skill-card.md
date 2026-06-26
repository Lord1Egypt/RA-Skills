## Description: <br>
Optimize vendor payment timing to maximize cash flow and capture early payment discounts by analyzing open AP, scoring discount opportunities, calculating annualized ROI, generating payment priority queues, and flagging late payment risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, accounting, and procurement users use this skill to review AP aging, decide which invoices to pay early, compare early payment discounts against cash costs, and build a cash-aware payment priority list. It is decision support only and does not send payments or sync to bank accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AP aging data can include sensitive vendor relationships, pricing, invoice amounts, and payment timing information. <br>
Mitigation: Use the skill only in appropriate business contexts and avoid sharing AP data outside approved finance or procurement workflows. <br>
Risk: Payment timing recommendations can be wrong if invoice terms, due dates, discount windows, cash availability, or cost-of-capital assumptions are inaccurate. <br>
Mitigation: Verify invoice terms and cash assumptions before acting on payment queues or discount recommendations. <br>
Risk: The skill may generate payment priorities or vendor-message suggestions that affect cash flow or supplier relationships. <br>
Mitigation: Require normal finance or procurement approval before sending vendor messages, importing payment CSVs, or making payments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/vendor-payment-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, CSV, Guidance] <br>
**Output Format:** [Markdown decision brief, full AP analysis report, or CSV payment queue] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decision support only; does not execute payments, access accounts, or send vendor messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
