## Description:

Adds self-custodied crypto payment checkout to a Next.js and Supabase app, including HD wallet address derivation, on-chain polling, and support for ETH, BTC, SOL, USDC, USDT, and other coins across nine chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flacko2048](https://clawhub.ai/user/flacko2048)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add a self-hosted crypto checkout flow to a Next.js 14+ App Router application backed by Supabase. It helps generate or wire in payment routes, database migrations, wallet derivation utilities, a checkout modal, and cron-based blockchain payment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment verification or fulfillment errors can create real financial loss or incorrect account credits.

Mitigation: Review and fix the payment verifier before production use, validate token decimals per chain, and make fulfillment transactionally idempotent.

Risk: The crypto wallet mnemonic is a single point of control for all derived deposit wallets.

Mitigation: Generate the mnemonic offline, store it only in a trusted secret manager, keep a secure offline backup, and prevent it from entering source code, logs, or client bundles.

Risk: The cron payment-check endpoint can be exposed if its authorization secret is weak or shared with an untrusted scheduler.

Mitigation: Use a strong CRON_SECRET, keep scheduler configuration trusted, and avoid giving the secret to third-party schedulers when that would exceed the deployment's risk tolerance.

Risk: External RPC and pricing calls introduce availability and data-integrity dependencies for payment confirmation.

Mitigation: Review the configured endpoints, pin and monitor provider choices, and fail closed when exchange-rate or balance checks cannot be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flacko2048/skills/self-hosted-crypto)
- [Publisher profile](https://clawhub.ai/user/flacko2048)
- [CoinGecko price API](https://api.coingecko.com/api/v3/simple/price)
- [mempool.space address API](https://mempool.space/api/address)
- [Etherscan](https://etherscan.io)
- [cr8claw](https://cr8claw.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, TSX, SQL, JSON, environment variable, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-specific file-copy, configuration, migration, and integration guidance; it does not execute payments directly.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
