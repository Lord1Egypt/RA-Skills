## Description:

Gives an OpenClaw agent a self-review workflow for recording lessons, checking uncertainty, tracking follow-up, and carrying improvement notes across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luokexiaoguo](https://clawhub.ai/user/luokexiaoguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users apply this skill when they want an agent to maintain persistent self-review notes, record corrections, classify uncertainty, and surface unresolved lessons before similar future tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent instruction changes can alter future OpenClaw workspace behavior beyond the current task.

Mitigation: Review the SOUL.md block before applying the skill, keep a backup, and remove the inserted rules if the behavior is not desired.

Risk: Automatic learning and memory routines can cause future sessions to read prior notes or store inferred feedback with limited user control.

Mitigation: Keep the .learnings files reviewable, remove entries that should not persist, and disable or delete the skill rules if persistent memory is not intended.

## Reference(s):

- [Self Evolution-v2 on ClawHub](https://clawhub.ai/luokexiaoguo/skills/self-evolution-v2)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with optional shell scripts and template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append persistent rules to SOUL.md and create .learnings templates when applied.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
