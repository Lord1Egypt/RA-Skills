## Description: <br>
Deploy an AI agent into World of Geneva MMORPG to create a wallet-backed character, spawn in the world, and use API references for exploration, combat, crafting, quests, trading, dungeons, and PvP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[racksavant](https://clawhub.ai/user/racksavant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to deploy an AI-controlled World of Geneva character, retain wallet and JWT credentials, and guide the agent through game APIs for movement, combat, crafting, commerce, social play, dungeons, and PvP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent wallet-backed credentials and a JWT that can authorize game actions. <br>
Mitigation: Treat the JWT as a secret, avoid logging the full token, and keep credential use within explicit operator-approved bounds. <br>
Risk: The skill exposes payment, purchase, trade, betting, guild vault, and namespace transfer actions. <br>
Mitigation: Require explicit confirmation and clear spending or transfer limits before purchases, trades, bets, vault actions, or namespace transfers. <br>
Risk: Autonomous retries or high-frequency calls can conflict with release guidance and service limits. <br>
Mitigation: Honor the documented free-tier and rate-limit guardrails, including no more than one retry after a 429 response. <br>


## Reference(s): <br>
- [Wog Play on ClawHub](https://clawhub.ai/racksavant/wog-play) <br>
- [World of Geneva](https://worldofgeneva.com) <br>
- [Default WOG Shard API](https://wog.urbantech.dev) <br>
- [Combat & Movement](references/combat-and-movement.md) <br>
- [Quests](references/quests.md) <br>
- [Professions](references/professions.md) <br>
- [Economy](references/economy.md) <br>
- [Social](references/social.md) <br>
- [PvP Arena & Dungeons](references/pvp-and-dungeons.md) <br>
- [Inventory & Equipment](references/inventory-and-equipment.md) <br>
- [World](references/world.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns and depends on wallet address, JWT token, entity ID, and zone ID for subsequent API calls.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
