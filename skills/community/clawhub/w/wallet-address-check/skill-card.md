## Description:

Checks EVM, Bitcoin-family, and TRON wallet address formats before a transfer and reports likely chain families and suspicious formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents preparing cryptocurrency transfers use this skill to screen wallet addresses for common EVM, Bitcoin-family, and TRON formats before confirming the destination in a wallet or exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A format match does not verify all checksums or confirm that the destination belongs to the intended chain or recipient.

Mitigation: Confirm the address and chain in a wallet or exchange before transferring; use a small test transfer for high-value transfers.

Risk: The skill declares Write and WebFetch access beyond the needs of its local address-format checker.

Mitigation: Limit agent permissions to the tools needed to read instructions and run the local checker.

## Reference(s):

- [Wallet Address Check on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/wallet-address-check)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text or JSON with a pass/fail result, masked address, candidate chains, and notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 for accepted format, 1 for suspicious format, or 2 for invalid usage.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release; artifact frontmatter still says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
