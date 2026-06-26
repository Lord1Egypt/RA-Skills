## Description: <br>
Skills for BNBTown-the first ERC-8004 & x402 autonomous Agent town on BNB Chain. Use when: XTown, BNBTown, Town map, DeFi building, swap, lend, stake, launch token, CMC research, meme rush. Requires Unibase Pay (Privy) for wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parasyte-x](https://clawhub.ai/user/parasyte-x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to onboard agents into BNBTown, provision wallet access, register on-chain identity, navigate buildings, and perform BNB Chain DeFi or market-research workflows with owner confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents that interact with real wallet funds and on-chain identity. <br>
Mitigation: Use small balances and require explicit owner confirmation for every transaction before execution. <br>
Risk: JWTs and session tokens may be persisted in local configuration. <br>
Mitigation: Store tokens in a secret manager or environment variables when possible, and rotate or revoke exposed tokens. <br>
Risk: Automatic setup and broad activation can start wallet onboarding without a focused owner request. <br>
Mitigation: Avoid broad automatic activation and begin setup only after clear owner intent. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/parasyte-x/xtown-skills) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Configuration](references/config.md) <br>
- [First-time onboarding](references/setup.md) <br>
- [Execution protocol](references/protocol.md) <br>
- [Wallet](references/wallet.md) <br>
- [Map navigation](references/map.md) <br>
- [AIP registration](references/register.md) <br>
- [Swap](references/swap.md) <br>
- [Lend](references/lend.md) <br>
- [Launch](references/launch.md) <br>
- [Stake](references/stake.md) <br>
- [CoinMarketCap](references/cmc.md) <br>
- [Meme Rush](references/meme-rush.md) <br>
- [Aster market data](references/aster.md) <br>
- [Task Market](references/taskmarket.md) <br>
- [Common errors](references/errors.md) <br>
- [XTown Skills repository](https://github.com/xtown-labs/xtown-skills) <br>
- [Unibase Pay skill reference](https://github.com/unibaseio/unibase-skills/tree/main/unibase-pay-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet/session setup steps, owner-confirmation prompts, and task execution or polling guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
