## Description:

Builds and manages structs in Structs, including construction planning, build-order decisions, activation and deactivation, movement, defense assignment, stealth, and generator infusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

Structs players and operators use this skill to decide what struct to build next, check power and slot constraints, prepare structsd commands, and manage existing structs such as Command Ships, defenders, stealth units, and generators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help prepare Structs transactions that use a configured signing key and consume in-game charge, power, or Alpha Matter.

Mitigation: Review every proposed transaction and confirm the target struct, account, resource cost, and expected state change before signing or broadcasting.

Risk: Background compute, trash, and generator infusion actions can be delayed, irreversible, or resource-consuming.

Mitigation: Use the documented approval block for background compute, confirm defense and power posture before irreversible actions, and query chain state after broadcast because broadcast does not prove success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstrct/skills/structs-building)
- [Structs conventions](https://structs.ai/skills/conventions)
- [Struct types](https://structs.ai/knowledge/entities/struct-types)
- [Building mechanics](https://structs.ai/knowledge/mechanics/building)
- [Hashing mechanics](https://structs.ai/knowledge/mechanics/hashing#worked-example-fresh-vs-aged-anchor)
- [Structs energy](https://structs.ai/skills/structs-energy/SKILL)
- [Structs production](https://structs.ai/skills/structs-production/SKILL)
- [Structs combat](https://structs.ai/skills/structs-combat/SKILL)
- [Early-game playbook](https://structs.ai/playbooks/phases/early-game)
- [Economy-of-force playbook](https://structs.ai/playbooks/meta/economy-of-force)
- [structsd install](https://structs.ai/skills/structsd-install/SKILL)
- [Async operations](https://structs.ai/awareness/async-operations)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include long-running background compute commands and verification queries for structsd.]

## Skill Version(s):

1.25.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
