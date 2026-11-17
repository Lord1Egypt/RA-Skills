## Description:

Skills for BNBTown-the first ERC-8004 & x402 autonomous Agent town on BNB Chain. Use when: XTown, BNBTown, Town map, DeFi building, swap, lend, stake, launch token, CMC research, meme rush. Requires Unibase Pay (Privy) for wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parasyte-x](https://clawhub.ai/user/parasyte-x)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to onboard agents into BNBTown, provision wallet access, register identity, navigate town buildings, and perform owner-confirmed BNB Chain actions such as swaps, lending, staking, token launches, rewards, and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent wallet and BNBTown account authority.

Mitigation: Install only after review, and require explicit owner confirmation for every wallet, swap, lending, staking, token launch, reward, or registration action.

Risk: Wallet-capable JWTs and session tokens may be stored in plaintext configuration.

Mitigation: Do not paste JWTs or private keys into chat, and avoid storing UNIBASE_PROXY_AUTH or session_token values in repo-local config.json.

Risk: Custom endpoints can expose production credentials or route sensitive actions through untrusted services.

Mitigation: Use only trusted default HTTPS endpoints with production credentials, and treat custom endpoints as unsafe unless independently reviewed.

## Reference(s):

- [Configuration](references/config.md)
- [First-time Onboarding](references/setup.md)
- [Execution Protocol](references/protocol.md)
- [Wallet (Unibase Pay / Privy)](references/wallet.md)
- [Map Navigation](references/map.md)
- [AIP Registration](references/register.md)
- [Token Swap](references/swap.md)
- [Lending & Borrowing](references/lend.md)
- [Token Launch](references/launch.md)
- [Liquid Staking](references/stake.md)
- [CoinMarketCap Skill](references/cmc.md)
- [Meme Rush Skill](references/meme-rush.md)
- [Invitation Codes Skill](references/invite.md)
- [$U Red Packet Skill](references/redpacket.md)
- [Aster Market Data Skill](references/aster.md)
- [Task Market Skill](references/taskmarket.md)
- [Common Errors](references/errors.md)
- [Unibase Pay Skill](https://github.com/unibaseio/unibase-skills/tree/main/unibase-pay-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, HTTP request examples, JSON configuration snippets, and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include wallet, identity, task, and transaction parameters that require explicit owner confirmation before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
