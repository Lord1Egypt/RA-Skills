## Description: <br>
Torch Domain Auction Bot discovers domains, launches them as Torch Market tokens, monitors lending positions, and can auto-liquidate underwater loans through a Torch Vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and DeFi operators use this skill to configure and run a Solana keeper for Torch Market domain tokens, lending health monitoring, vault-routed liquidation, and lease rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor can spend vault SOL on eligible liquidations and launch domain tokens on Solana mainnet. <br>
Mitigation: Install only when this mainnet keeper behavior is intended; use a disposable linked wallet, keep the vault authority key out of the bot environment, fund conservatively, and set conservative thresholds. <br>
Risk: The skill uses external network egress for Solana RPC and read-only market, identity, and domain data. <br>
Mitigation: Review egress policy before running, use trusted RPC providers, and monitor logs for unexpected endpoint or transaction behavior. <br>
Risk: Liquidation and domain lease rotation can have irreversible economic consequences. <br>
Mitigation: Require explicit user initiation, test on a fork or controlled setup first, and verify vault linkage, risk threshold, and profit threshold before enabling continuous monitoring. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/mrsirg97-rgb/torchdomainauctionbot) <br>
- [Torch Market Website](https://torch.market) <br>
- [Torch Market Docs](https://torch-market-docs.vercel.app) <br>
- [Kit Source Link from Metadata](https://github.com/mrsirg97-rgb/torch-domain-auction-bot) <br>
- [Design Document](artifact/design.md) <br>
- [Security Audit](artifact/audit.md) <br>
- [Formal Verification Report](artifact/verification.md) <br>
- [Whitepaper](artifact/whitepaper.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands, TypeScript snippets, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user initiation; monitor actions depend on Solana RPC, vault linkage, and configured thresholds.] <br>

## Skill Version(s): <br>
2.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
