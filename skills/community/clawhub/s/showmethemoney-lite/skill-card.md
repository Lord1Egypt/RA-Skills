## Description: <br>
ShowMeTheMoney Lite guides users through a StablePay-backed paid demo flow with wallet setup, visible pricing, a free preview, and payment confirmation before premium output. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[bubblevan](https://clawhub.ai/user/bubblevan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to test a monetized OpenClaw skill flow: previewing a paid action, configuring StablePay wallet prerequisites, approving payment, and receiving a premium demo result only after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can lead the user into a real StablePay-style payment flow. <br>
Mitigation: Confirm the price, currency, merchant DID, and endpoint values before approval, and use test funds or strict spending limits where possible. <br>
Risk: The skill is a weak-protection demo and includes placeholder merchant configuration. <br>
Mitigation: Replace placeholders before real use, require StablePay backend confirmation for purchase status, and do not treat local wallet or policy state as proof of payment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API Calls] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include StablePay payment-flow calls and must wait for payment confirmation before premium output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
