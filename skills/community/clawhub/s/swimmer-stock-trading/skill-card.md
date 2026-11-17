## Description:

Swimmer Custodial Stock Orders helps agents discover Swimmer Finance Solana stock-token routes and balances, prepare market or limit orders, and submit explicit custodial transfer instructions while warning that settlement is non-atomic and off-chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytx1991](https://clawhub.ai/user/ytx1991)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Swimmer Finance Solana stock-token availability, check wallet balances, prepare order plans, and submit explicitly authorized custodial transfers from a dedicated low-balance wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill can irreversibly send real Solana tokens to a custodial recipient.

Mitigation: Use a dedicated low-balance wallet, authorize only the exact transfer amount and digest intended, and stop if the recipient cannot be independently verified.

Risk: The submitted transaction is not an atomic swap and cannot guarantee execution, cancellation, refund, or delivery of requested tokens.

Mitigation: Review current Swimmer custody and settlement terms from official sources, treat signatures as submitted rather than settled, and verify settlement status separately before retrying.

Risk: A private key or wallet config exposed to chat or logs can compromise funds.

Mitigation: Never paste secrets into the agent conversation; keep the config in the fixed protected path with exact 0700 directory and 0600 file permissions.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/ytx1991/skills/swimmer-stock-trading)
- [Swimmer Finance](https://swimmer.finance)
- [Solana Mainnet RPC Endpoint](https://api.mainnet-beta.solana.com)
- [SharesDAO Discovery API Origin](https://api.sharesdao.com:8443)
- [Solana Mainnet Balances](references/balances.md)
- [Custody, Settlement, and Counterparty Risk](references/custody-and-settlement.md)
- [Dedicated Wallet and Policy Setup](references/keypair-setup.md)
- [Solana USDC Route Discovery and Memo Protocol](references/protocol.md)
- [Inspect, Authorize, and Submit](references/wallet-submission.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON plan, inspection, balance, and submission summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, Solana mainnet network access, Swimmer discovery API access, and a protected local wallet config.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
