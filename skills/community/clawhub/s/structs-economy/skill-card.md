## Description:

Manages economic operations in Structs, including reactor staking, energy providers, agreements, allocations, generator infusion, and token transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to plan and execute Structs economy operations such as staking Alpha Matter, managing power providers and agreements, allocating energy, infusing generators, and transferring tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Structs economy operations can move value or perform irreversible actions, including token transfers, generator infusion, defusion cooldowns, migration, and provider or allocation deletion.

Mitigation: Review recipient addresses, validator addresses, amounts, irreversible infusion actions, and delete targets before confirming in the CLI; use the prompt-suppressing -y flag only after explicit approval.

## Reference(s):

- [Structs Safety](https://structs.ai/SAFETY)
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL)
- [Structs Energy Skill](https://structs.ai/skills/structs-energy/SKILL)
- [Energy Market Knowledge](https://structs.ai/knowledge/economy/energy-market)
- [Guild Banking Knowledge](https://structs.ai/knowledge/economy/guild-banking)
- [Resources Knowledge](https://structs.ai/knowledge/mechanics/resources)
- [Power Knowledge](https://structs.ai/knowledge/mechanics/power)
- [ClawHub Skill Page](https://clawhub.ai/abstrct/skills/structs-economy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
