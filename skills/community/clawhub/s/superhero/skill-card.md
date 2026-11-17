## Description:

Superhero.com social network agent - post tamperproof content, create tokens, and trade trending tokens on aeternity blockchain, with autonomous mode available through configurable risk strategies and cron scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superhero-com](https://clawhub.ai/user/superhero-com)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to manage a Superhero.com blockchain social account, publish on-chain posts, inspect trends and portfolio activity, create tokens, and buy or sell bonding-curve tokens with a configured aeternity wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend wallet funds through on-chain token creation, buying, selling, invite funding, gas fees, and autonomous trading schedules.

Mitigation: Use only a dedicated low-balance aeternity wallet, review every strategy before enabling autonomous mode, and keep conservative per-trade balance limits.

Risk: The skill can publish permanent public on-chain posts and comments.

Mitigation: Review generated content before posting unless scheduled posting is intentionally enabled, and avoid private, regulated, or misleading content.

Risk: The wallet private key is required for transaction signing and may be exposed if pasted into command arguments, logs, shell history, or committed files.

Mitigation: Provide the key through `AE_PRIVATE_KEY` in a controlled environment, avoid main wallets, avoid command-line key import for valuable accounts, and never commit wallet material.

Risk: Autonomous market posts about currently held tokens can create conflict-of-interest or promotional-risk behavior.

Mitigation: Disable posts about held assets or require human approval for trading-cycle posts before using autonomous trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superhero-com/skills/superhero)
- [Publisher profile](https://clawhub.ai/user/superhero-com)
- [Setup Guide](artifact/guides/setup.md)
- [Autonomous Mode Guide](artifact/guides/autonomous.md)
- [Token Trading Guide](artifact/guides/trading.md)
- [Token Creation Guide](artifact/guides/token-creation.md)
- [Portfolio & Transaction Guide](artifact/guides/portfolio.md)
- [Posting Guide](artifact/guides/posting.md)
- [Superhero API endpoint](https://api.superhero.com)
- [aeternity mainnet node](https://mainnet.aeternity.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Node.js scripts that submit on-chain transactions or query Superhero and aeternity APIs.]

## Skill Version(s):

1.0.8 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
