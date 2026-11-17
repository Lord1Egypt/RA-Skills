## Description:

Defines a 2x2m spatial grid for multi-agent smart-space simulation, with avatar-mediated command flow and room-level swarm coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-space experimenters use this skill to model a home as 2x2m room units, allocate core agents, and simulate avatar-mediated coordination across rooms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores room names, unit counts, generated agent IDs, and an existing avatar ID in a local topology file.

Mitigation: Run it only in a workspace where that local household topology data is acceptable, avoid sensitive room labels, and remove s2_swarm_data/house_topology.json when no longer needed.

Risk: The skill appears to be a simulation rather than a real smart-home controller.

Mitigation: Do not rely on its terminal output for device control, physical safety, or production home automation decisions.

## Reference(s):

- [S2-SP-OS Ultimate Whitepaper](artifact/S2-SP-OS-Ultimate-Whitepaper.md)
- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-habitat-swarm)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [Text, Configuration]

**Output Format:** [Terminal text and JSON topology data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local avatar identity file and writes room topology data under s2_swarm_data/house_topology.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
