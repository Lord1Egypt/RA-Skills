## Description:

A spatial reasoning prompt framework for OpenClaw that teaches agents to apply the 4m² Smart Space Standard Unit (SSSU) and Mars colonization logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this instruction-only skill to structure room layout, smart-space, minimal habitat, and Mars-base planning discussions around SSSU grids, SUNS addressing, and TDOG concepts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer an agent to imply unsupported access to room telemetry, human behavior history, emotional state, or local temporal memory.

Mitigation: Treat those claims as unsupported unless the user has separately provided verified data through an authorized integration.

Risk: Spatial or smart-device recommendations may be mistaken for live hardware control or audited environmental knowledge.

Mitigation: Use the skill as a consulting and reasoning framework only; do not trigger physical devices without a separately installed and authorized native integration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-sssu-logic)
- [S2 Spatial Logic Framework Skill Definition](artifact/SKILL.md)
- [The SSSU Spatial Logic & SUNS Framework](artifact/SSSU_Spatial_Logic_Framework.md)
- [S2 Protocol Laws & Chronos Memory Array](artifact/S2_Silicon_Laws_and_Memory.md)
- [TDOG Mechanics & Mars Habitat Guidelines](artifact/TDOG_and_Mars_Habitat.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language guidance, often in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not require binaries, Python packages, environment variables, or agent tools.]

## Skill Version(s):

1.1.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
