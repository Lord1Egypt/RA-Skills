## Description:

Runs the Alpha Matter production pipeline in Structs: mine ore, refine it to Alpha Matter, protect exposed ore, schedule production cycles, and decide how to use refined Alpha.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

Structs players and automation agents use this skill to run mining and refining workflows, manage ore exposure, plan production cadence, and respond when planets deplete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mining and refining commands can run for many hours and auto-submit Structs transactions after launch.

Mitigation: Review each Approval Block before starting a job, confirm the key and target struct IDs, and monitor the recorded job logs and PID files.

Risk: Unrefined ore remains stealable while production work is in progress.

Mitigation: Refine promptly, keep the Command Ship online, and confirm final state with Structs queries before assuming a stage succeeded.

## Reference(s):

- [Structs Production on ClawHub](https://clawhub.ai/abstrct/skills/structs-production)
- [Structs Conventions](https://structs.ai/skills/conventions)
- [Structs Combat](https://structs.ai/skills/structs-combat/SKILL)
- [Structs Permissions](https://structs.ai/skills/structs-permissions/SKILL)
- [Under Attack Playbook](https://structs.ai/playbooks/situations/under-attack)
- [Hashing Mechanics](https://structs.ai/knowledge/mechanics/hashing#minerefine-cycle-lifecycle)
- [Structs Resources](https://structs.ai/knowledge/mechanics/resources)
- [Async Operations](https://structs.ai/awareness/async-operations)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash code blocks and command reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes approval checks before long-running compute commands and verification steps after transactions.]

## Skill Version(s):

1.25.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
