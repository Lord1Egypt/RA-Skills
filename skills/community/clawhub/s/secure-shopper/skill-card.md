## Description: <br>
Asynchronous shopping research and optional checkout using secure-autofill, with shopping results recorded to workspace artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moodykong](https://clawhub.ai/user/moodykong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to delegate shopping research across configured retail sites, compare candidate items, and optionally continue to checkout after explicit accept and confirmation gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved shopping artifacts may contain sensitive shopping preferences, delivery context, candidate URLs, and order status. <br>
Mitigation: Avoid unnecessary sensitive details in prompts and periodically delete old secure_shopping artifacts. <br>
Risk: Checkout can submit real orders using secure-autofill. <br>
Mitigation: Verify item, price, quantity, shipping address, delivery date, and payment method before confirming checkout. <br>


## Reference(s): <br>
- [Secure Shopper ClawHub page](https://clawhub.ai/moodykong/secure-shopper) <br>
- [Publisher profile](https://clawhub.ai/user/moodykong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON shopping artifacts and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records candidate items, accept/deny status, and checkout phase in secure_shopping workspace artifacts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
