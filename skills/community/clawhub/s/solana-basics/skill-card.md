## Description:

Interact with Solana blockchain via Helius APIs. Create/manage wallets, check balances (SOL + tokens), send transactions, swap tokens via Jupiter, and monitor addresses. Use for any Solana blockchain operation, crypto wallet management, token transfers, DeFi swaps, or portfolio tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chattyclaw](https://clawhub.ai/user/chattyclaw)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage Solana wallets, query balances and assets, send SOL or SPL tokens, request swap quotes, and execute token swaps through Helius and Jupiter integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real wallet keys and on-chain transactions with weak key protection.

Mitigation: Do not use wallets holding meaningful funds unless key storage is changed to a user passphrase, hardware wallet, OS keychain, or another strong secret store.

Risk: Transaction safety controls are insufficient for irreversible blockchain transfers.

Mitigation: Decode transaction details, validate recipients, amounts, fees, and token mints, and require explicit user confirmation before signing or sending transactions.

Risk: Swap execution signs a transaction returned by a remote API without independent instruction verification.

Mitigation: Treat swaps as high risk; verify the route, decoded instructions, slippage, and expected token amounts before signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chattyclaw/skills/solana-basics)
- [Helius API Reference](references/helius-api.md)
- [Jupiter Swap Integration](references/jupiter.md)
- [Wallet Security Best Practices](references/security.md)
- [Helius Dashboard](https://dashboard.helius.dev/signup)
- [Jupiter Quote API](https://api.jup.ag/swap/v1/quote)
- [Jupiter Swap API](https://api.jup.ag/swap/v1/swap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that interact with live Solana wallets, Helius APIs, and Jupiter swap APIs.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
