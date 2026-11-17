## Description:

Calculates, validates, and visualizes wall-mounted faucet installation geometry, especially faucet reach L and outlet height H1 for product selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starsy](https://clawhub.ai/user/starsy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, installers, and developers use this skill to calculate wall-mounted faucet reach, outlet height, drain position, basin setback, and stream angle. It also supports annotated SVG diagrams for client or installer handoff before on-site verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The faucet layout result is a straight-line geometric estimate and may not reflect final water behavior, pressure, aerator design, or field conditions.

Mitigation: Confirm final placement with a full-scale mock-up or on-site water-flow test before concealed installation.

Risk: Generated diagrams can be confused across projects if saved with generic filenames.

Mitigation: Use clear project-specific output filenames for SVG diagrams and review the annotated dimensions before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/starsy/skills/wall-mounted-faucet-layout-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/starsy)
- [Skill instructions](artifact/SKILL.md)
- [English geometry diagram](artifact/assets/wall_mounted_faucet_geometry_v2.svg)
- [Chinese geometry diagram](artifact/assets/wall_mounted_faucet_geometry_v2_zh.svg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown/text responses with optional bash commands and generated SVG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses one consistent length unit for calculations; generated diagrams should use clear project-specific filenames.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
