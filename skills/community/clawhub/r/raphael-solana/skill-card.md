## Description:

Manage Solana and Polygon wallets, run Polymarket weather arbitrage, post to X/Twitter, and execute Raydium swaps from natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inspi-writer001](https://clawhub.ai/user/inspi-writer001)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent manage Solana and Polygon wallets, check balances, prepare transfers, run Polymarket weather-arbitrage scans, and operate X/Twitter posting workflows. It is intended for users who can review and approve high-impact wallet, trading, and social-media actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control funded Solana and Polygon wallets, including swaps, transfers, and Polymarket orders.

Mitigation: Start with empty or low-balance wallets, use dry-run mode first, and require explicit user approval before live swaps, transfers, or orders.

Risk: The skill can post or reply from an X/Twitter account.

Mitigation: Verify account permissions, keep posting strategies in dry-run during setup, and enable live posting only when public-account impact is acceptable.

Risk: Credential setup can expose wallet and X/Twitter secrets if run in logged terminals or CI.

Mitigation: Avoid running setup in shared logs or CI, protect MASTER_ENCRYPTION_PASSWORD_CRYPTO and X credentials, and verify custom RPC and wallet storage paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/inspi-writer001/skills/raphael-solana)
- [Publisher Profile](https://clawhub.ai/user/inspi-writer001)
- [X Developer Platform](https://developer.x.com)
- [DexScreener API Endpoint](https://api.dexscreener.com/latest/dex)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, JSON-like tool parameters, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger plugin tool calls or local CLI commands when an agent follows the skill.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
