## Description: <br>
Reconciles broker commission statements against expected loan-level payouts, flags discrepancies, and produces a concise summary with follow-up actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-chi](https://clawhub.ai/user/li-chi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Revenue operations, broker payment, and lending teams use this skill to reconcile broker commission statements against expected loan-level payouts before approving payouts or investigating discrepancies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive commission, loan, and payout data may be exposed if unnecessary source fields are provided. <br>
Mitigation: Limit inputs to the fields needed for reconciliation and process only statements and exports the user is permitted to handle. <br>
Risk: Incorrect matches or variance calculations could lead to wrong payout decisions. <br>
Mitigation: Treat results as decision support and have a qualified person verify variances, ambiguous matches, and unusual adjustments before approving or changing payments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/li-chi/reconcile-broker-commission-statement) <br>
- [Publisher profile](https://clawhub.ai/user/li-chi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table and summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reconciled rows, status categories, variance totals, key findings, and recommended next actions.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
