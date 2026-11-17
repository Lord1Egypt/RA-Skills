## Description:

Guides agents through Spraay Gateway payment validation, fee estimates, price and chain queries, and user-approved batch payouts, payroll, and escrow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payment operators use this skill to validate and estimate multi-recipient crypto payouts, inspect token prices and chain status, and prepare user-approved payouts or escrow through Spraay Gateway. Free lookups need no key; paid operations require a subscription key or separately approved x402 payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect recipients or amounts could cause costly fund transfers.

Mitigation: Verify recipient addresses, amounts, token, chain, and estimated fees; require a fresh explicit confirmation of the exact preview before each payout, escrow, or payroll operation.

Risk: Paid endpoints and x402 calls can incur service charges beyond the funds transferred.

Mitigation: Disclose subscription or per-call costs and obtain explicit approval for each x402 spend; leave subscription checkout to the user.

Risk: Disclosure of the Spraay API key could allow unauthorized gateway access.

Mitigation: Treat SPRAAY_API_KEY as sensitive, send it only to the official HTTPS gateway, and never request private keys or seed phrases.

## Reference(s):

- [Spraay Gateway endpoint examples](artifact/references/endpoints.md)
- [Spraay Gateway documentation](https://docs.spraay.app)
- [Spraay Gateway](https://gateway.spraay.app)
- [ClawHub skill release](https://clawhub.ai/plagtech/skills/spraay-gateway)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with curl examples and plain-language payment previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a free validation and fee estimate plus explicit user confirmation before any fund-moving request.]

## Skill Version(s):

1.0.2 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
