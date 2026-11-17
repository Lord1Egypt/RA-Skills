## Description:

Enables agents to shop through CreditClaw payment rails, owner approval flows, and platform-specific checkout guides for Shopify and other merchants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent controlled shopping and seller-payment capabilities through CreditClaw, including merchant detection, checkout approval, card handoff, x402 signing, and store or payment-link management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent real payment authority, including purchases through CreditClaw rails.

Mitigation: Install only for intended payment use, keep approval set to ask-for-everything, and configure merchant restrictions and spending limits before use.

Risk: The Shopify-facing label understates the broader shopping, selling, card-handling, and checkout-instruction scope.

Mitigation: Review the full bundled skill scope before deployment, including shopping, checkout, x402 wallet, webhook, and store/payment-link files.

Risk: Card-handling workflows and decryption steps can expose sensitive payment data if mishandled.

Mitigation: Use only approved checkout flows, avoid logging or persisting decrypted card data, and verify deletion of any checkout sub-agent after completion.

Risk: Seller, payment-link, and public-store APIs can create pages that collect money.

Mitigation: Do not enable or use seller and public-store features unless money-collection behavior is explicitly desired and reviewed.

Risk: Remote vendor Markdown or delivered decryption scripts may alter checkout behavior.

Mitigation: Independently verify remote vendor instructions and scripts before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/triplehippo/skills/shopify-pay2)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw API base](https://creditclaw.com/api/v1)
- [Main skill evidence](artifact/SKILL.md)
- [Checkout guide evidence](artifact/CHECKOUT-GUIDE.md)
- [Shopping guide evidence](artifact/SHOPPING-GUIDE.md)
- [OpenClaw checkout evidence](artifact/agents/OPENCLAW.md)
- [Stripe x402 wallet evidence](artifact/STRIPE-X402-WALLET.md)
- [Store and payment-link evidence](artifact/MY-STORE.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces purchase, checkout, wallet, webhook, merchant-routing, and store-management guidance for an agent; normal use requires CREDITCLAW_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
