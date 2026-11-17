## Description:

Execute token swaps using the 0x API with support for price quotes, gasless meta-transactions, and on-chain trade history retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch 0x swap quotes, prepare token-swap commands, and execute ERC-20 swaps across supported EVM chains using configured API keys and wallet credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend real wallet funds automatically and was classified as suspicious by the authoritative security evidence because transaction checks are weak.

Mitigation: Review each transaction before signing, inspect quote destination, calldata, value, RPC chain, and token decimals, and use a dry-run or explicit confirmation workflow before using real funds.

Risk: The skill requires private wallet credentials in environment variables.

Mitigation: Use a dedicated low-balance wallet, avoid exporting valuable private keys in shared shells, and keep credentials out of logs and persistent shell history.

Risk: Dependency or API behavior could change without a pinned lockfile.

Mitigation: Install from a reviewed dependency set, prefer a pinned lockfile, and review changes to 0x API responses before executing swaps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aviclaw/skills/zeroex-swap)
- [0x Developer Dashboard](https://dashboard.0x.org/)
- [0x Swap API](https://api.0x.org/swap/permit2/quote)
- [0x Gasless API](https://api.0x.org/gasless/quote)
- [0x Trade Analytics Swap API](https://api.0x.org/trade-analytics/swap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JavaScript examples, API request examples, and transaction status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate live 0x API requests and signed blockchain transactions when used with real API keys, RPC endpoints, and wallet credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
