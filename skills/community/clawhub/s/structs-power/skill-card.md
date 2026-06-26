## Description: <br>
Manages power infrastructure in Structs. Covers substations, allocations, player connections, and power monitoring. Use when power is low or overloaded, creating or managing substations, connecting players to substations, allocating capacity, diagnosing offline status, or planning power budget for new structs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Structs players and operators use this skill to assess power state, manage substations and allocations, connect or migrate players, and recover from low-power or overloaded infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Power transactions can affect live Structs infrastructure and may take players or downstream systems offline if signed incorrectly. <br>
Mitigation: Run transactions interactively, verify entity IDs and power amounts before signing, and avoid -y unless the exact action has been approved. <br>
Risk: Delete, disconnect, and migrate operations can cascade across substations, allocations, or other players. <br>
Mitigation: Coordinate before disconnecting or migrating players, confirm every target belongs in the requested operation, and disconnect dependent allocations or players before deleting substations. <br>


## Reference(s): <br>
- [Structs Power Skill Page](https://clawhub.ai/abstrct/structs-power) <br>
- [Structs Safety](https://structs.ai/SAFETY) <br>
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL) <br>
- [Structs Energy Skill](https://structs.ai/skills/structs-energy/SKILL) <br>
- [Structs Power Mechanics](https://structs.ai/knowledge/mechanics/power) <br>
- [Structs Building Mechanics](https://structs.ai/knowledge/mechanics/building) <br>
- [Structs Resource Mechanics](https://structs.ai/knowledge/mechanics/resources) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
