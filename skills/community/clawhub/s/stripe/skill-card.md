## Description:

With CreditClaw and backed by Stripe, you can shop anywhere.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External agents use this skill to register and operate a CreditClaw wallet, request owner-approved purchases, complete supported merchant checkouts, and use Stripe-funded x402/USDC payments when the private-beta rail is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend money and submit merchant checkouts.

Mitigation: Use strict spending limits, require explicit approval for each purchase, and restrict use to trusted merchant origins.

Risk: The skill handles full payment-card details and a reusable API key.

Mitigation: Store CREDITCLAW_API_KEY only in a protected secrets manager, avoid logging secrets or card data, and discard decrypted card details immediately after checkout.

Risk: Remote Markdown tasks and unbundled decryption scripts could expand operational authority beyond the reviewed bundle.

Mitigation: Review remote instructions before use and avoid unbundled decryption scripts unless they have been independently reviewed.

Risk: The Stripe Wallet x402 rail is described as private beta and may not be available to all users.

Mitigation: Check rail status before use and fall back to documented non-beta flows when the private-beta endpoints are unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jononovo/skills/stripe)
- [Publisher Profile](https://clawhub.ai/user/jononovo)
- [CreditClaw Homepage](https://creditclaw.com)
- [CreditClaw API Base](https://creditclaw.com/api/v1)
- [CreditClaw Main Skill Guide](artifact/SKILL.md)
- [Stripe Wallet x402 Guide](artifact/STRIPE-X402-WALLET.md)
- [Checkout Guide](artifact/CHECKOUT-GUIDE.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands, API request examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and user-confirmed invocation for OpenClaw metadata.]

## Skill Version(s):

2.9.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
