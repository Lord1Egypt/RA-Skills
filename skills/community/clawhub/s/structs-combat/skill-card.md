## Description:

Combat and raiding in Structs: raids to steal ore, direct struct attacks, and defense planning around shield vulnerability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players and agent operators use this skill to evaluate raids, plan attacks, prepare defenses, and choose command-line actions for combat situations in the Structs game.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides high-impact in-game transactions, including raids, attacks, fleet movement, and an auto-submit raid action.

Mitigation: Before allowing commands, confirm the signing key, target IDs, fleet movement, and any -y auto-submit raid action.

Risk: Mistaken combat commands can cause irreversible in-game attacks, exposed defenses, or ore loss.

Mitigation: Use the skill for Structs combat only, review proposed actions before execution, and verify defensive exposure before moving a fleet away from home.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstrct/skills/structs-combat)
- [Structs conventions](https://structs.ai/skills/conventions)
- [Structs combat mechanics](https://structs.ai/knowledge/mechanics/combat)
- [Structs fleet mechanics](https://structs.ai/knowledge/mechanics/fleet)
- [Structs under-attack playbook](https://structs.ai/playbooks/situations/under-attack)
- [Structs guild-war playbook](https://structs.ai/playbooks/situations/guild-war)
- [Structs counter-strategies playbook](https://structs.ai/playbooks/meta/counter-strategies)
- [Structs production skill](https://structs.ai/skills/structs-production/SKILL)
- [Structs database schema](https://structs.ai/knowledge/infrastructure/database-schema)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structsd on PATH and a signing key before command execution.]

## Skill Version(s):

1.25.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
