## Description:

SMFOI-KERNEL provides a 5-step orientation protocol that helps agents track workspace boundaries, safety constraints, user intent, action priority, and local audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rigeneproject](https://clawhub.ai/user/rigeneproject)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to add a repeatable orientation check to autonomous agent workflows. It is intended to keep each turn grounded in workspace limits, active constraints, user intent, and human-reviewed protocol evolution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Every-turn activation can affect all agent interactions after installation.

Mitigation: Review the skill before deployment and install it only where an always-on orientation layer is desired.

Risk: Local audit logs may retain orientation outcomes across turns.

Mitigation: Review or clear ./memory/kernel/state.md when retained orientation history is not wanted.

Risk: Protocol optimization suggestions could be mistaken for self-executing changes.

Mitigation: Treat Level 3 proposals as human-reviewed text suggestions and apply changes manually only after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rigeneproject/skills/smfoi-kernel)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Orientation logic](artifact/kernel_v0.2.txt)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown and plain text procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Activates every turn and may record orientation outcomes under ./memory/kernel/state.md when local logging is used.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact files identify protocol version 0.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
