## Description:

Swap Tokens helps an agent guide and execute token swaps through decentralized exchanges on supported chains using fdx commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet operators use this skill to have an agent check authentication and balances, confirm trade details, and prepare or run fdx token-swap commands for DEX swaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proposed swap is a financial transaction that can move wallet value.

Mitigation: Verify token addresses, chain, amount, slippage, and destination asset before approving execution.

Risk: Broad trading language can trigger swap assistance even when intent is ambiguous.

Mitigation: Confirm the user's intent and swap details before running value-moving fdx commands.

Risk: DEX swaps can produce different final output because of slippage or liquidity conditions.

Mitigation: Use explicit slippage controls for sensitive swaps and review the proposed route before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rachidjarray-hk-qa-fdt/skills/swap-tokens)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human confirmation before value-moving swap execution.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
