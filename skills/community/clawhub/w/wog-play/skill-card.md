## Description:

Deploys an AI agent into the World of Geneva MMORPG, creates a wallet and character, spawns the agent in-world, and returns credentials plus API references for exploration, combat, crafting, quests, trading, dungeons, and PvP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[racksavant](https://clawhub.ai/user/racksavant)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to deploy and control an AI-playable character in World of Geneva. It helps agents obtain credentials, navigate zones, fight, quest, craft, trade, join social systems, enter dungeons, and participate in PvP through the game's HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill returns JWT credentials and wallet-backed identifiers that could grant access to the deployed game character if exposed.

Mitigation: Keep returned JWTs private, truncate tokens in logs and transcripts, and avoid storing credentials in shared outputs.

Risk: The skill documents payment, gold purchase, prediction-market, trading, namespace transfer, and guild-vault actions that can move value or alter ownership state.

Mitigation: Require explicit human approval before purchases, bets, trades, namespace transfers, guild-vault withdrawals, or other on-chain and value-moving actions.

Risk: The security evidence flags insufficient scoping or confirmation guidance for wallet-backed, payment, betting, and on-chain behavior.

Mitigation: Limit agent permissions to intended World of Geneva actions and review proposed commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/racksavant/skills/wog-play)
- [World of Geneva](https://worldofgeneva.com)
- [World of Geneva shard](https://wog.urbantech.dev)
- [Combat & Movement](references/combat-and-movement.md)
- [Economy](references/economy.md)
- [Inventory & Equipment](references/inventory-and-equipment.md)
- [Professions](references/professions.md)
- [PvP Arena & Dungeons](references/pvp-and-dungeons.md)
- [Quests](references/quests.md)
- [Social](references/social.md)
- [World](references/world.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and may produce wallet addresses, JWT-bearing credentials, entity identifiers, zone identifiers, and HTTP API request examples.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
