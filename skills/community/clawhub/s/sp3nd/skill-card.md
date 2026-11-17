## Description:

Purchase shipped products and tokenized Collector Crypt cards through SP3ND with USDC on Solana using server-priced carts, payment-ready order gates, and fulfillment tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kent-x1](https://clawhub.ai/user/kent-x1)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to create SP3ND carts and orders for Amazon, eBay, and Collector Crypt purchases, pay approved USDC quotes, and track shipped-product or wallet-delivered fulfillment. It is intended for real checkout flows where server-authoritative pricing, idempotency, wallet attribution, and payment status must be respected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real USDC payments for shipped products and Collector Crypt cards.

Mitigation: Use a dedicated least-funded wallet, set explicit spending limits or human approval rules, and pay only after SP3ND returns a current payment-ready quote.

Risk: API credentials, wallet key material, shipping details, and contact details are sensitive.

Mitigation: Keep SP3ND credentials and wallet files private, avoid logging or committing secrets, and provide shipping or contact data only for the intended checkout.

Risk: Retrying after a timeout or ambiguous settlement can create payment uncertainty.

Mitigation: Preserve idempotency keys and signed transaction bytes, read the order before retrying, and retry only the identical authorized payment when the API allows it.

Risk: Collector Crypt payment confirms SP3ND treasury receipt but does not itself prove NFT delivery.

Mitigation: Continue polling until the order is delivered with asset transfer evidence, and do not buy replacement cards or transfer assets outside the documented fulfillment flow.

Risk: Collector Crypt listings can sell or change before manual acquisition is completed.

Mitigation: Refresh expired or changed quotes, reconfirm changed totals against the user's authorization, and let SP3ND handle review or refunds.

## Reference(s):

- [Published ClawHub Skill](https://clawhub.ai/kent-x1/skills/sp3nd)
- [Collector Crypt checkout](references/collector-crypt.md)
- [SP3ND API documentation](https://sp3nd.shop/partner-api/docs)
- [SP3ND Agent Card](https://sp3nd.shop/.well-known/agent-card.json)
- [Published SP3ND skill](https://sp3nd.shop/skill.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with HTTP examples, JSON request and response examples, JavaScript code, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SP3ND API credentials and may use a Solana wallet state file for payment examples.]

## Skill Version(s):

1.11.0 (source: evidence.release.version, artifact SKILL.md metadata.version, clawhub.json version, agent-card.json version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
