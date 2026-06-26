## Description: <br>
Agent banking and payments on Solana. Send and receive stablecoins with cancellable escrow transfers. Optional on-chain accounts with policy-enforced spending limits for human-delegated automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silostack](https://clawhub.ai/user/silostack) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use SilkyWay to manage Solana USDC wallets, send or claim cancellable escrow payments, and operate delegated payment accounts with human-set spending limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can give an agent real-money signing authority for Solana payments. <br>
Mitigation: Start on devnet, keep mainnet balances limited, and require human review before any real USDC send, withdrawal, claim, cancellation, or delegated account transfer. <br>
Risk: Wallet private keys are stored in a local configuration file. <br>
Mitigation: Protect ~/.config/silkyway/config.json with local access controls and avoid sharing its contents or other secrets in chat. <br>
Risk: Transactions are built by the SilkyWay API before local signing. <br>
Mitigation: Confirm the configured cluster and API URL before use, and check that SILK_API_URL has not been overridden unexpectedly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/silostack/silkyway) <br>
- [SilkyWay homepage](https://silkyway.ai) <br>
- [SilkyWay API base](https://api.silkyway.ai) <br>
- [SilkyWay devnet API base](https://devnet-api.silkyway.ai) <br>
- [npm package @silkysquad/silk](https://www.npmjs.com/package/@silkysquad/silk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, the silk CLI, network access to SilkyWay APIs, and a funded Solana wallet for payment operations.] <br>

## Skill Version(s): <br>
1.0.9 (source: evidence release, frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
