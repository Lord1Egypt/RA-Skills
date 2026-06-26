## Description: <br>
Order groceries from Zepto in seconds. Just say what you need, get a payment link on WhatsApp, pay on your phone, done. Remembers your usual items. Works across India where Zepto delivers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bewithgaurav](https://clawhub.ai/user/bewithgaurav) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to automate Zepto grocery shopping in a logged-in browser session, including address confirmation, cart building, payment-link generation, and order follow-up. <br>

### Deployment Geography for Use: <br>
India, where Zepto delivers <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate in a logged-in Zepto browser session and may act on the user's grocery account. <br>
Mitigation: Confirm the delivery address, cart contents, total, and payment link before proceeding, and use a separate browser profile or clear the session when persistent access is not desired. <br>
Risk: Smart-shop and clear-cart flows can remove existing cart items. <br>
Mitigation: Check the cart before adding items and get clear user confirmation before clearing items except where the user has explicitly approved post-payment cleanup. <br>


## Reference(s): <br>
- [ClawHub Zepto Skill](https://clawhub.ai/bewithgaurav/zepto) <br>
- [Zepto Website](https://www.zepto.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and user-facing checkout guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-automation steps, cart summaries, address confirmation prompts, payment-link instructions, and local order-history guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
