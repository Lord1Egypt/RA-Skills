## Description:

Zepto helps an agent order groceries from Zepto by confirming the delivery address, managing cart items, generating a payment link, and sending it over WhatsApp for user payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bewithgaurav](https://clawhub.ai/user/bewithgaurav)

### License/Terms of Use:

MIT

## Use Case:

External users in India use this skill to delegate Zepto grocery shopping tasks to an agent while retaining control over address confirmation and payment approval. The skill supports repeat grocery ordering by using local order history to suggest usual items.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The skill controls an authenticated Zepto browser session and can change shopping-account state.

Mitigation: Require explicit user confirmation before address changes, cart changes, checkout, payment-link generation, and order-history scraping.

Risk: Cart clearing may remove items the user intended to keep.

Mitigation: Show current cart contents and ask whether to keep or clear existing items before removal.

Risk: Payment-link workflows can lead to unintended purchases if the user does not inspect the order.

Mitigation: Have the user review cart contents, delivery address, total price, and the payment link before completing payment manually.

Risk: Local order history may retain shopping preferences.

Mitigation: Tell users where the local order-history file is stored and support clearing it when they no longer want retained shopping context.

## Reference(s):

- [ClawHub Zepto skill page](https://clawhub.ai/bewithgaurav/skills/zepto)
- [ClawHub publisher profile](https://clawhub.ai/user/bewithgaurav)
- [Zepto website](https://www.zepto.com)
- [Zepto account page](https://www.zepto.com/account)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw browser control and may use WhatsApp messaging for payment links.]

## Skill Version(s):

1.0.6 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
