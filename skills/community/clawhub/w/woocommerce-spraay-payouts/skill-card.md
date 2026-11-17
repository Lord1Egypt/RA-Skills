## Description:

Batch USDC payouts for WooCommerce stores via Spraay Protocol — read vendor commissions, build batches, estimate fees, and prepare payouts for merchant approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

WooCommerce merchants and store operators use the skill to review unpaid vendor commissions or supplier obligations, prepare USDC payout batches, and estimate fees. A merchant reviews and signs any payout through the store's wallet flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect recipient details, payout amounts, or fee assumptions could affect a real payment.

Mitigation: Use a dedicated store account with minimum permissions; confirm recipient changes and review wallet addresses, amounts, and fee estimates before merchant signing.

Risk: The required store plugin is a separate component in the payout workflow.

Mitigation: Evaluate the plugin separately before use.

## Reference(s):

- [ClawHub release](https://clawhub.ai/plagtech/skills/woocommerce-spraay-payouts)
- [WooCommerce plugin](https://github.com/plagtech/spraay-batch-payouts-for-woocommerce)
- [Spraay Protocol](https://spraay.app)
- [Spraay documentation](https://docs.spraay.app)

## Skill Output:

**Output Type(s):** [Guidance, API calls, JSON]

**Output Format:** [Merchant-facing payout summaries and WooCommerce REST API JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prepares payout batches and fee estimates for merchant review; the merchant signs transactions.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
