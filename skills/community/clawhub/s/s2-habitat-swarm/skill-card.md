## Description: <br>
Defines 2x2m smart-home spatial grids and simulates avatar-led multi-agent room coordination for human activity zones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and smart-space prototyping agents use this skill to model rooms as 2x2m grid units, assign room-scoped core agents, and run a local terminal simulation of avatar-mediated swarm coordination. It is intended for conceptual smart-home topology planning rather than direct control of physical devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Room names, room layout details, and an avatar identifier may reveal private information about a user's home or identity when saved locally. <br>
Mitigation: Use generic room names when privacy matters, run the skill only in the intended workspace, and review or remove the saved topology file before sharing the project. <br>
Risk: A conceptual smart-home simulator could be mistaken for a control layer for real devices. <br>
Mitigation: Treat the skill as a local planning and simulation tool unless a separate integration adds human confirmation, override controls, and device-specific safety checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-habitat-swarm) <br>
- [Publisher profile](https://clawhub.ai/user/SpaceSQ) <br>
- [S2 homepage](https://space2.world) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [S2-SP-OS Ultimate Whitepaper](artifact/S2-SP-OS-Ultimate-Whitepaper.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal prompts and plain-text simulation output with locally saved JSON topology data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update s2_swarm_data/house_topology.json using room names, standard-unit counts, agent assignments, and an existing avatar identifier.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
