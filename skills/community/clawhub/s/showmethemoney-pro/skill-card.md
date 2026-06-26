## Description: <br>
Executes the paid ShowMeTheMoney premium action through a merchant backend, using StablePay when payment is required before retrying the protected action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bubblevan](https://clawhub.ai/user/bubblevan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run a protected ShowMeTheMoney action, handle required StablePay payment, and present the unlocked result or store information returned by the backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate StablePay payments for the premium action and for individual reports. <br>
Mitigation: Review the displayed price and currency, rely only on backend-returned payment requirements, and keep local StablePay limits and confirmation settings enabled. <br>
Risk: Optional request text may be forwarded to the merchant backend. <br>
Mitigation: Do not include secrets or confidential text in q or prompt fields, and install only when the local merchant backend is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bubblevan/showmethemoney-pro) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Markdown or plain text response based on the backend result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate a StablePay purchase flow and retries the protected action once after successful payment.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
