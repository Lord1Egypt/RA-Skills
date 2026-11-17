## Description:

Helps agents record pay-on-delivery agreements through the Spraay gateway and guide a payer through verifying delivery and signing a USDC transfer on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can create, check, fund, release, cancel, or list pay-on-delivery agreement records. Payers verify delivery and approve a wallet-signed USDC payment; beneficiaries can distinguish gateway status from confirmed payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Escrow terms and wallet addresses are sent to the Spraay gateway and may be visible through gateway lookups.

Mitigation: Share only necessary agreement details and avoid sensitive information in terms or conditions.

Risk: Funds are not locked; funded or released status does not prove that a beneficiary has been paid.

Mitigation: Do not treat gateway status as proof of payment; verify a confirmed USDC transfer on Base before reporting payment complete.

Risk: Paid calls and wallet signing can incur fees or transfer funds.

Mitigation: Check the payment challenge and transfer details locally, obtain explicit user approval, and sign only the verified transaction.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/plagtech/skills/spraay-escrow)
- [Spraay documentation](https://docs.spraay.app)
- [Spraay app](https://spraay.app)
- [Spraay x402 discovery](https://gateway.spraay.app/.well-known/x402.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payment and signing steps require user confirmation; payment is established only by a confirmed Base transfer.]

## Skill Version(s):

1.0.1 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
