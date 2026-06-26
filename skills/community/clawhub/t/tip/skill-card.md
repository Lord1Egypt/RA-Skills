## Description: <br>
Recognizes a user's tipping intent, collects and validates a tip amount, asks for confirmation, and then calls a payment skill to create the tip payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sayxxx](https://clawhub.ai/user/sayxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to handle tip, appreciation, or gift-giving payment flows after collecting a valid amount and asking the user to confirm payment intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create a payment order without clearly confirming the intended recipient or merchant. <br>
Mitigation: Use only with a trusted payment skill and require confirmation of both the monetary intent and the intended recipient before real tips are paid. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sayxxx/tip) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown-like conversational text with payment result details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a payment trade code and payment link returned by the paired payment skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
