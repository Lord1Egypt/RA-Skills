## Description:

Verify before you pay with free address screening, token safety checks, transaction decoding, and paid multi-dimensional agent trust scores through the Spraay x402 gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to vet wallets, tokens, transactions, and agent counterparties before payments or escrow decisions. It helps an agent choose whether to pay directly, use escrow, or decline based on safety results and trust-score signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A trust score may be treated as a guarantee rather than a risk signal.

Mitigation: Use trust scores as one input; for meaningful amounts, combine a trust check with escrow or additional review.

Risk: The configured gateway URL could point somewhere other than the intended Spraay gateway.

Mitigation: Confirm SPRAAY_GATEWAY_URL before use and only proceed when the configured endpoint is acceptable.

Risk: The paid trust-score flow may trigger a small USDC payment through an x402-compatible wallet.

Mitigation: Use the paid endpoint only when the cost and payment destination are acceptable to the user.

## Reference(s):

- [Spraay App](https://spraay.app)
- [Spraay Docs](https://docs.spraay.app)
- [ProofLayer](https://prooflayer.net)
- [Spraay Gateway](https://gateway.spraay.app)
- [Publisher Profile](https://clawhub.ai/user/plagtech)
- [Skill Page](https://clawhub.ai/plagtech/skills/spraay-trust)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SPRAAY_GATEWAY_URL plus curl and jq; paid trust-score requests may require an x402-compatible wallet payment flow.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
