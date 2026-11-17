## Description:

Whispers from the Star is a Chinese-language xianxia text adventure skill that guides an agent through cultivation realms, character growth, inventory handling, reincarnation, and choice-driven narrative play.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouwenjie03](https://clawhub.ai/user/ouwenjie03)

### License/Terms of Use:


## Use Case:

External users and role-playing agents use this skill to run a Chinese-language cultivation text RPG with persistent character, inventory, and biography state. It is intended for interactive story play, branching choices, and xianxia scenario generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gameplay can modify the local game_state.md save file during normal use.

Mitigation: Back up game_state.md before play or before major story decisions if preserving a run matters.

Risk: Inventory rules may discard in-game items when the backpack is full and the player gives an unclear choice.

Mitigation: Give explicit item names or numbers when resolving inventory prompts, and review the resulting game_state.md if item preservation is important.

## Reference(s):

- [Whispers from the Star ClawHub Page](https://clawhub.ai/ouwenjie03/skills/whispers-from-the-star)
- [Game Start and Initialization](references/ch00_start.md)
- [Qi Refining Realm Journey](references/ch01_qi_refining.md)
- [Foundation Building Realm Journey](references/ch02_foundation.md)
- [Golden Core Realm Journey](references/ch03_golden_core.md)
- [Nascent Soul Realm Journey](references/ch04_nascent_soul.md)
- [Spirit Transformation Realm Journey](references/ch05_spirit_transformation.md)
- [Tribulation Realm Journey](references/ch06_tribulation.md)
- [Ascension Realm Journey](references/ch07_ascension.md)
- [Managing Character System](references/system_character_system.md)
- [Managing Inventory System](references/system_inventory_system.md)
- [Managing Biography System](references/system_biography_system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Interactive Markdown narrative with local Markdown save-state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language gameplay; reads bundled chapter and system files and may update a local game_state.md save file during play.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
