## Description: <br>
Interact with Solana blockchain via Helius APIs. Create/manage wallets, check balances (SOL + tokens), send transactions, swap tokens via Jupiter, and monitor addresses. Use for any Solana blockchain operation, crypto wallet management, token transfers, DeFi swaps, or portfolio tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chattyClaw](https://clawhub.ai/user/chattyClaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to manage Solana wallets, inspect balances and assets, send SOL or SPL tokens, execute Jupiter swaps, and monitor wallet activity through Helius-backed APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move funds through Solana sends and Jupiter swaps. <br>
Mitigation: Use a test or low-value wallet, require manual approval for every send or swap, and verify recipient addresses, mints, amounts, slippage, fees, and network before signing. <br>
Risk: The security review flags weak safeguards around locally stored wallet keys. <br>
Mitigation: Replace default key storage with passphrase-protected storage, an OS keychain, or a hardware wallet before funding any wallet managed by this skill. <br>
Risk: API keys can be exposed if real keys are placed in URLs or logs. <br>
Mitigation: Keep API keys in local configuration, avoid logging request URLs that contain keys, and rotate any key that may have been exposed. <br>
Risk: Unpinned or unaudited dependencies can increase operational risk for funded wallets. <br>
Mitigation: Pin and audit dependencies before using this skill with wallets that hold real value. <br>


## Reference(s): <br>
- [Helius API Reference](references/helius-api.md) <br>
- [Jupiter Swap Integration](references/jupiter.md) <br>
- [Wallet Security Best Practices](references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript examples and CLI command patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Helius API key and local wallet/configuration files for operational use.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
