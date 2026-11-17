## Description:

Search flights and stays, then create card or crypto payments via TravAI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirikov](https://clawhub.ai/user/kirikov)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to search flights or stays, compare travel options, confirm pricing, and create TravAI card or crypto payment flows through an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create payment and itinerary records without a clearly required final user authorization step.

Mitigation: Before any payment is created, require an explicit user confirmation after presenting the exact offer, price, conditions, traveller details, payment method, and token/network when crypto is used.

Risk: Use of the skill may send TravAI login tokens, traveller identity and contact details, travel search data, wallet addresses, and payment-session information.

Mitigation: Use only when the user is comfortable sharing those details with TravAI, and avoid collecting or sending unnecessary personal or payment information.

Risk: Expired searches, offers, or rates can produce invalid bookings or stale pricing.

Mitigation: Re-run searches and use fresh search, offer, and rate IDs when an offer is expired, not found, or pricing cannot be confirmed.

Risk: Crypto payments can fail or be misdirected if the amount, token, network, deposit address, or refund wallet is altered.

Mitigation: Present the exact amount, token, network, deposit address, and refund wallet without rounding or substitution, and ask the user to confirm them before payment.

## Reference(s):

- [TravAI live OpenAPI schema](https://api.travai.tech/openapi.json)
- [TravAI ClawHub skill page](https://clawhub.ai/kirikov/skills/travai-search-book-pay-flights-stays)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown instructions with JSON request examples and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking, payment, refund-wallet, and support-contact instructions for TravAI workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
