## Description:

Swap tokens and read pool state on Uniswap V4 across Base, Ethereum mainnet, and Base Sepolia, including pool discovery, quotes, Permit2 approvals, and exact-input swaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect Uniswap V4 pools, estimate swap output, manage Permit2 approvals, and execute exact-input swaps on supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real, long-lived token approvals and sign irreversible transactions when PRIVATE_KEY is provided.

Mitigation: Use a dedicated low-balance wallet, review token, amount, recipient, slippage, chain, and spender before write operations, avoid auto-approve unless the allowance risk is understood, and revoke allowances after use.

Risk: Unsafe legacy shell scripts remain in the artifact.

Mitigation: Use the TypeScript entry points under src/ and do not run the legacy shell scripts or bootstrap curl-to-bash recommendation.

Risk: Private keys or transaction details may be exposed through public logs.

Mitigation: Provide PRIVATE_KEY only through environment variables or a secret manager and treat stdout and stderr as public logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclaw-consensus-bot/skills/uniswap-v4)
- [Uniswap V4 deployments](https://docs.uniswap.org/contracts/v4/deployments)
- [Contract addresses](references/addresses.md)
- [V4 architecture](references/v4-architecture.md)
- [V4 encoding reference](references/v4-encoding.md)
- [Clanker token deployments](https://clanker.gitbook.io/clanker-documentation/general/token-deployments)
- [Clanker creator rewards and fees](https://clanker.gitbook.io/clanker-documentation/general/creator-rewards-and-fees)
- [Clanker deployed contracts](https://clanker.gitbook.io/clanker-documentation/references/deployed-contracts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and TypeScript command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe read-only checks, transaction preparation, approval setup, or swap execution steps; write operations require private-key-backed signing outside public logs.]

## Skill Version(s):

2.0.4 (source: CHANGELOG.md, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
