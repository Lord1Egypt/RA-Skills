## Description:

Manages planets and fleets in Structs, including planet evaluation and exploration, claiming or relocation, fleet movement and composition, evacuation, and onStation-versus-away decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players use this skill to decide when to explore or replace planets, move fleets, evaluate fleet posture, and prepare CLI transactions for planet and fleet operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subsequent planet exploration is destructive and can remove the current planet and planet-bound structs.

Mitigation: Keep subsequent planet exploration interactive, confirm currentOre is 0, confirm the fleet is onStation, and move or accept loss of anything worth keeping before signing.

Risk: Fleet movement or away posture can expose the home planet and block build, mine, refine, and explore actions.

Mitigation: Review destination and transaction details before signing, refine stored ore before leaving when appropriate, and recall the fleet home when defense or planet operations are needed.

## Reference(s):

- [Structs Planets & Fleet on ClawHub](https://clawhub.ai/abstrct/skills/structs-planets-fleet)
- [Structs planet mechanics](https://structs.ai/knowledge/mechanics/planet)
- [Structs fleet mechanics](https://structs.ai/knowledge/mechanics/fleet)
- [Structs command conventions](https://structs.ai/skills/conventions)
- [structsd install](https://structs.ai/skills/structsd-install/SKILL)
- [Structs production skill](https://structs.ai/skills/structs-production/SKILL)
- [Structs combat skill](https://structs.ai/skills/structs-combat/SKILL)
- [Structs mid-game playbook](https://structs.ai/playbooks/phases/mid-game)
- [Structs under-attack playbook](https://structs.ai/playbooks/situations/under-attack)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes structsd is installed, on PATH, and configured with a signing key.]

## Skill Version(s):

1.25.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
