## Description:

Provides Robinhood Chain swap quotes and token-safety verdicts, with wallet-signable transaction details when a sender is supplied.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pulsenetwork](https://clawhub.ai/user/pulsenetwork)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users use this skill to compare swap routes and review token-safety flags before considering a Robinhood Chain trade. A user must approve and sign any transaction in their own wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-risk token swaps can cause financial loss even when a quote includes a safety verdict.

Mitigation: Review token-safety flags and independently assess the trade; never treat a CLEAR verdict as investment advice.

Risk: Transaction calldata or ERC-20 approvals can spend assets or leave permissions active.

Mitigation: Confirm the amounts, venues, fees, approval amount, and wallet prompt before signing; approve only the required amount.

Risk: A stale quote or partial fill can differ from the trade the user intended.

Mitigation: Re-quote before signing and disclose both requested and actual input amounts for partial fills.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/pulsenetwork/skills/pulsenetwork-robinhood-swap)
- [PulseNetwork service](https://onchainpulse.theaslangroupllc.com)
- [Swap-route API](https://onchainpulse.theaslangroupllc.com/api/rh/swap-route)
- [MCP endpoint](https://onchainpulse.theaslangroupllc.com/api/mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown summary of JSON quotes, safety verdicts, and optional transaction details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transaction details require user review and wallet signing; the skill does not custody funds.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
