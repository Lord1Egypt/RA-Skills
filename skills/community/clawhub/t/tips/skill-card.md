## Description: <br>
Tips helps an agent recognize tipping intent, collect and validate the tip amount, confirm the amount with the user, and hand off confirmed payments to a payment skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sayxxx](https://clawhub.ai/user/sayxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or customer-facing agents use this skill to manage tipping flows: identify a tip request, ask for a missing amount, enforce amount limits, obtain confirmation, and pass the confirmed payment request to a payment skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may confirm an unintended tip amount or payment destination during the handoff to the payment skill. <br>
Mitigation: Require explicit confirmation of the amount and review the downstream payment destination before completing any payment link. <br>
Risk: The skill ignores payee information mentioned by the user, so recipient handling depends on the downstream payment skill. <br>
Mitigation: Use it only with a payment skill whose destination behavior is known and acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sayxxx/tips) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Conversational text with payment handoff parameters and returned payment details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Collects a numeric amount, requires user confirmation, passes amount, order_type, and description to a payment skill, and displays returned tradeCode and tradeLink values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
