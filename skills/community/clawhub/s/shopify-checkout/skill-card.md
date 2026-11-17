## Description:

Complete online shopping purchases on any online store using the Credpay Checkout API with x402 payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jelilat](https://clawhub.ai/user/jelilat)

### License/Terms of Use:


## Use Case:

External users use this skill to complete online purchases by providing product, contact, shipping, and payment details so an agent can request a quote, submit checkout, and report order status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may share email, phone, shipping address, product details, and payment information with Credpay.

Mitigation: Show the user the personal and checkout data that will be sent and obtain confirmation before submitting checkout requests.

Risk: The skill may authorize USDC payments on Base, including an additional payment if the final order total exceeds the quoted amount.

Mitigation: Require explicit user confirmation of the recipient, token, chain, total amount, maximum payment amount, and any extra charge before sending an x402 payment.

Risk: Creating more than one checkout for the same intent can duplicate purchase attempts.

Mitigation: Track the active requestId and do not start another checkout for the same user intent until the current request completes or fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jelilat/skills/shopify-checkout)
- [Credpay Checkout API base URL](https://checkout-agent.credpay.xyz)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown guidance with HTTP request examples and JSON checkout status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires product details, email, shipping address, goods total, and explicit x402 payment authorization; checkout status is polled until completion, failure, or timeout.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
