## Description:

Explores new planets and manages fleet movement in Structs. Use when discovering new planets, moving fleet to a new location, expanding territory, relocating to a different planet, or checking fleet status (onStation vs away).

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players and operators use this skill to plan planet exploration, fleet relocation, and status checks while preserving transaction confirmation safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed Structs transactions can move fleets or explore planets using player, fleet, planet, and destination IDs.

Mitigation: Verify every ID before signing and prefer the interactive CLI confirmation flow for transaction commands.

Risk: Subsequent planet exploration can release the old planet, destroy remaining structs, and scatter fleets.

Mitigation: Confirm currentOre is 0, the fleet is onStation, and all valued structs have been moved or intentionally abandoned before exploring.

Risk: Fleet movement to unscouted or hostile space can strand assets in enemy range.

Mitigation: Scout destination and nearby hostile state with planet and fleet queries before moving to uncertain locations.

## Reference(s):

- [Structs Safety](https://structs.ai/SAFETY)
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL)
- [Planet mechanics](https://structs.ai/knowledge/mechanics/planet)
- [Fleet mechanics](https://structs.ai/knowledge/mechanics/fleet)
- [Entity relationships](https://structs.ai/knowledge/entities/entity-relationships)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes transaction commands, verification queries, and approval checkpoints; no files are produced.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
