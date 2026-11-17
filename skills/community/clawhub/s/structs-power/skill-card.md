## Description:

Manages power infrastructure in Structs. Covers substations, allocations, player connections, and power monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players and operators use this skill to assess power state, manage substations and allocations, connect or migrate players, and recover from low-power or overloaded conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Power-management transactions can change live game or account state, including taking players or substations offline.

Mitigation: Review transaction details before execution, prefer interactive confirmations, and avoid -y unless there is explicit approval for the exact action.

Risk: Disconnecting, deleting, or migrating allocations and players can cascade to downstream capacity loss.

Mitigation: Coordinate disruptive actions with affected players and disconnect allocations or players deliberately before deletion workflows.

## Reference(s):

- [Structs Power Skill on ClawHub](https://clawhub.ai/abstrct/skills/structs-power)
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL)
- [Structs Energy Skill](https://structs.ai/skills/structs-energy/SKILL)
- [Structs Power Mechanics](https://structs.ai/knowledge/mechanics/power)
- [Structs Building Mechanics](https://structs.ai/knowledge/mechanics/building)
- [Structs Resource Mechanics](https://structs.ai/knowledge/mechanics/resources)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Analysis]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
