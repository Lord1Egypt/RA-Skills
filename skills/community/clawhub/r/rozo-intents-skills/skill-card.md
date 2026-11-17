## Description:

ROZO Intents Pay & Bridge helps agents send and bridge USDC/USDT via Rozo, check supported wallet balances, parse crypto payment QR codes, and check Rozo payment status across supported EVM, Solana, and Stellar networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnmuggle](https://clawhub.ai/user/shawnmuggle)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers use this skill to send or bridge stablecoin payments via Rozo, check USDC/USDT balances, parse payment QR codes, and track Rozo payment status while confirming irreversible crypto transfer details before funding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto transfers are irreversible, and a wrong address, chain, token, memo, or amount can cause unrecoverable loss.

Mitigation: Show the full payment details and require explicit user confirmation before funding; keep the shipped confirmation thresholds at 0 unless the user intentionally accepts no-confirmation payments.

Risk: The skill sends wallet addresses, payment details, status identifiers, and Stellar trustline checks to external services.

Mitigation: Run balance, payment, and status checks only when the user requests them, and disclose that financial metadata is sent to Rozo APIs and Horizon as part of the workflow.

Risk: Untrusted QR, address, or memo text can be unsafe if interpolated into shell commands.

Mitigation: Pass user-controlled values as safely quoted command arguments and avoid shell interpolation when invoking the documented Node.js scripts.

Risk: The security review flags optional no-confirmation execution and an unaudited external wallet-funding command as review concerns.

Mitigation: Review the funding path before deployment, require user verification of payment details, and leave no-confirmation execution disabled unless deliberately accepted.

## Reference(s):

- [ROZO Intents Pay & Bridge](https://clawhub.ai/shawnmuggle/skills/rozo-intents-skills)
- [Rozo API Reference](artifact/references/api-reference.md)
- [Supported Tokens and Chains](artifact/references/supported-chains.md)
- [Wallet Address Detection Rules](artifact/references/wallet-detection.md)
- [Rozo](https://rozo.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls]

**Output Format:** [Markdown guidance with inline shell commands and structured payment, balance, QR parsing, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; normal operation transmits wallet addresses, chain and token choices, amounts, memos, and payment IDs to Rozo APIs.]

## Skill Version(s):

1.0.9 (source: evidence release, artifact frontmatter, version.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
