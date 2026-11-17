## Description:

文字角色扮演游戏 (Text RPG) - 基于 sbordeyne/rpg-text 项目的面向对象设计，融合原始D&D规则。AI作为DM引导回合制冒险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[beancookie](https://clawhub.ai/user/beancookie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and role-playing game players use this skill to run a Chinese-language text RPG where the agent acts as dungeon master, guides character creation, resolves turn-based exploration and combat, and summarizes in-game progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: English-only users may misunderstand Chinese-language commands, game text, or summaries.

Mitigation: Ask the agent to translate commands and gameplay text before relying on them.

Risk: Generated game-state summaries may be incomplete or inconsistent during extended play.

Mitigation: Review character state, inventory, quests, and progress summaries before treating them as saved state.

## Reference(s):

- [D&D Rules Reference](references/dnd-rules.md)
- [Monster Reference](references/monsters.md)
- [Item Reference](references/items.md)
- [Spell Reference](references/spells.md)
- [Game Timer Data](references/data/game_timer.json)
- [Items Data](references/data/items.json)
- [Jobs Data](references/data/jobs.json)
- [Maps Data](references/data/maps.json)
- [Monsters Data](references/data/monsters.json)
- [Extended Monsters Data](references/data/monsters_extended.json)
- [Monster Parties Data](references/data/monster_parties.json)
- [Quests Data](references/data/quests.json)
- [Races Data](references/data/races.json)
- [Save Format Data](references/data/save_format.json)
- [Shops Data](references/data/shops.json)
- [Spells Data](references/data/spells.json)
- [Status Effects Data](references/data/status_effects.json)
- [Treasures Data](references/data/treasures.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational Markdown/text with game commands, narration, turn results, and progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language interactive RPG output based on static game data and normal game-state summaries.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
