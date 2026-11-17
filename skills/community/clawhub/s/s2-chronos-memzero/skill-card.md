## Description:

Archives one-minute, delta-compressed spatial state data with causal event logs for a local S2 Chronos memory simulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-space system designers use this skill to simulate an S2-style local memory layer that records environment state changes, agent decisions, avatar mandates, and external video pointers in SQLite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Life-safety memory claims are stronger than the implemented logging and compression controls support.

Mitigation: Review the skill before installing it in smart-home, safety, incident-review, or compliance workflows; treat it as a simulation unless independent safety controls are added.

Risk: The database may omit relevant environmental changes because repeated or below-threshold state changes can be folded.

Mitigation: Validate sampling, thresholds, and event-bypass behavior against the target environment before relying on the resulting timeline.

Risk: Retention and privacy controls are described in configuration but are not fully enforced by the demonstrated script.

Mitigation: Add operational retention, access-control, and audit checks around generated SQLite data before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-chronos-memzero)
- [Project homepage](https://space2.world)
- [Skill documentation](artifact/SKILL.md)
- [English Chronos memory whitepaper](artifact/S2-SP-OS-ltimate-Whitepaper.md)
- [Chinese Chronos memory whitepaper](artifact/S2 时空全息记忆阵列白皮书.md)
- [Chronos configuration](artifact/chronos_config.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Markdown guidance, Python execution behavior, SQLite database records, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local SQLite state under s2_memory_vault when the Python script is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
