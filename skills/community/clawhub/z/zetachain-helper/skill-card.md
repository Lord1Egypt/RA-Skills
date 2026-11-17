## Description:

ZetaChain omnichain helper for asset balance lookup, CCTX cross-chain tracking, zEVM deployment guidance, and technical documentation indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mango-ice-cat](https://clawhub.ai/user/mango-ice-cat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ZetaChain users use this skill to query omnichain balances, track CCTX transaction status, and obtain practical guidance for ZetaChain workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses, optional BTC addresses, and CCTX hashes may be sent to public blockchain RPC, LCD, and API providers.

Mitigation: Use only addresses and transaction hashes appropriate for public lookup, and disclose the providers before running network-backed commands.

Risk: Advertised guidance and implemented lookup behavior may not fully match.

Mitigation: Treat generated workflow guidance as advisory and verify implementation-sensitive steps against current ZetaChain documentation before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mango-ice-cat/skills/zetachain-helper)
- [thirdweb ZetaChain RPC endpoint](https://zetachain.rpc.thirdweb.com)
- [BlockPI ZetaChain LCD endpoint](https://zetachain.blockpi.network/lcd/v1/public)
- [Blockstream Bitcoin API endpoint](https://blockstream.info/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code examples, and JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query public blockchain RPC, LCD, and API providers for wallet addresses, optional BTC addresses, and CCTX hashes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
