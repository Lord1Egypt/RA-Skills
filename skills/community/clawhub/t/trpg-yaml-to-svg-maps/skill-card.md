## Description:

Generates static SVG visual maps from existing TRPG YAML map data, including nodes, edges, regions, labels, arrows, and readable Traditional Chinese text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, game masters, and TRPG content authors use this skill to turn YAML scenario map data into browser-viewable SVG maps for tabletop play and rulebook material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated maps may misrepresent relationships or locations when YAML files omit node coordinates.

Mitigation: Review each SVG against the source YAML and scenario initial_map references before using it in play or published material.

Risk: The skill writes new SVG files alongside source YAML maps.

Mitigation: Use version control or a workspace diff to confirm original YAML files were not modified and only intended SVG outputs were added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ice26985850/skills/trpg-yaml-to-svg-maps)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Standard SVG files generated alongside source YAML maps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads YAML maps under maps/ and scenario initial_map references, estimates missing node coordinates when needed, and does not modify original YAML files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
