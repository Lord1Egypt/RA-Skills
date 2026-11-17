## Description:

Tempo stablecoin and token swap operations for agents. Use when working with pathUSD/USDC.e balances, swapping between USDC.e and pathUSD, or executing any-token swaps via Uniswap on Tempo with quote, Permit2 approvals, simulation, and broadcast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check Tempo stablecoin balances, transfer pathUSD, quote swaps, prepare Permit2 approvals, simulate transactions, and broadcast Uniswap swaps on Tempo mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact wallet transactions and private key handling can move funds or expose credentials.

Mitigation: Use a dedicated low-value wallet, avoid shared shells for private keys, and require explicit confirmation before any cast send command.

Risk: Broad token approvals or incorrect spender/router addresses can create unintended token access.

Mitigation: Approve exact amounts for short durations, verify spender and router addresses, and decode calldata before signing.

Risk: The skill installs Foundry through a remote installer.

Mitigation: Install Foundry through a verified channel and review the installer source before use.

## Reference(s):

- [Tempo RPC Endpoint](https://rpc.presto.tempo.xyz)
- [Foundry Installer](https://foundry.paradigm.xyz)
- [Uniswap Trade API Quote Endpoint](https://trade-api.gateway.uniswap.org/v1/quote)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with shell commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied PRIVATE_KEY and UNISWAP_API_KEY; transaction commands require explicit review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
