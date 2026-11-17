## Description:

Interact with Uniswap v4 pools and liquidity positions on QELT Mainnet for DEX pool queries, token swaps, WQELT wrapping, position NFTs, and contract address lookup, with only Uniswap V4 supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prqelt](https://clawhub.ai/user/prqelt)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query QELT Mainnet Uniswap v4 pool state, retrieve contract addresses, prepare swaps, manage WQELT wrapping, and prepare liquidity-position workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad token approvals in liquidity workflows can leave user funds exposed.

Mitigation: Prefer exact token amounts, short approval deadlines, confirmed transaction receipts, and revoke allowances after use.

Risk: Prepared swaps, wrapping, and liquidity changes are irreversible once signed and broadcast.

Mitigation: Review transaction data before signing, confirm chain ID 770, verify spender and contract addresses, and apply slippage and deadline limits.

Risk: Private keys or unsigned sensitive wallet material could be exposed if provided to an agent.

Mitigation: Use only pre-signed raw transactions for write operations and never provide private keys.

## Reference(s):

- [QELT DEX ClawHub release](https://clawhub.ai/prqelt/skills/qelt-dex)
- [QELTScan](https://qeltscan.ai)
- [Uniswap v4 Contract Addresses - QELT Mainnet](artifact/references/contracts.md)
- [Uniswap v4 SDK Examples - QELT Mainnet](artifact/references/sdk-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, TypeScript, JSON-RPC examples, and contract address tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose RPC calls and pre-signed transaction submission flows; does not require or handle private keys.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
