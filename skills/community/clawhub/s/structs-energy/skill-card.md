## Description:

Power and capacity in Structs — getting more energy, fixing "I'm offline", substations and allocations, load budgeting, and reactor/generator infusion for your own capacity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players and operators use this skill to diagnose offline power states, plan capacity headroom, infuse reactors or generators, and configure substations and allocations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following the skill can lead to signed Structs transactions that spend, lock, move, or irreversibly consume assets.

Mitigation: Review transaction prompts, amounts, validator addresses, struct IDs, and signing accounts before approving any transaction.

Risk: Generator infusion and substation or allocation changes can affect player or guild power availability.

Mitigation: Confirm capacity headroom and the intended allocation or substation target before changing power routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstrct/skills/structs-energy)
- [Structs energy mechanics](https://structs.ai/knowledge/mechanics/energy)
- [Structs power mechanics](https://structs.ai/knowledge/mechanics/power)
- [Structs resource mechanics](https://structs.ai/knowledge/mechanics/resources)
- [Structs conventions](https://structs.ai/skills/conventions)
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL)
- [Structs resource-rich playbook](https://structs.ai/playbooks/situations/resource-rich)
- [Structs commerce skill](https://structs.ai/skills/structs-commerce/SKILL)
- [Structs building skill](https://structs.ai/skills/structs-building/SKILL)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction review steps for Structs energy operations.]

## Skill Version(s):

1.25.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
