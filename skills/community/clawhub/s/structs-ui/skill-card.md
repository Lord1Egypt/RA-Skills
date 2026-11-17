## Description:

Structs UI helps agents build dashboards, forms, menus, HUDs, and companion clients for the Structs universe using SUI and client references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Structs-style UI surfaces and client code for dashboards, forms, menus, HUDs, signing workflows, proof-of-work, and GRASS event consumption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated client code may involve wallet signing and transaction queues.

Mitigation: Review transaction code carefully and keep explicit user confirmation around real signing actions.

Risk: Multiple or premature transaction submissions can cause sequence or charge-gating failures.

Mitigation: Serialize signing actions, wait for confirmed last-action height, and surface transaction failures to the operator.

## Reference(s):

- [Structs UI documentation](https://structs.ai/develop/ui/)
- [Structs UI tokens](https://structs.ai/develop/ui/tokens)
- [Structs UI icons](https://structs.ai/develop/ui/icons)
- [Structs UI components](https://structs.ai/develop/ui/components)
- [Structs UI runtime](https://structs.ai/develop/ui/runtime)
- [Structs UI gotchas](https://structs.ai/develop/ui/gotchas)
- [Structs client documentation](https://structs.ai/develop/client/)
- [Structs actions and signing](https://structs.ai/develop/client/actions-and-signing)
- [Structs proof-of-work](https://structs.ai/develop/client/work-and-pow)
- [Structs realtime GRASS](https://structs.ai/develop/client/realtime-grass)
- [Structs repositories](https://structs.ai/develop/repos)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, commands, and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UI implementation guidance, client integration guidance, transaction-signing cautions, proof-of-work workflow advice, and review checklists.]

## Skill Version(s):

1.25.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
