## Description:

Self helps an agent maintain an evolving SELF.md self-model through scheduled reflection checks, meaningful trigger criteria, and lightweight reliability guards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirchlive](https://clawhub.ai/user/kirchlive)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add persistent personality-growth reflection to an agent workspace while keeping durable identity boundaries separate from living observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent self-memory can influence future agent behavior without enough consent or review.

Mitigation: Enable the skill only in workspaces where persistent agent memory is intended and review SELF.md, HEARTBEAT.md, AGENTS.md, and memory files before relying on them.

Risk: Self-observation files may accumulate user-specific or confidential details.

Mitigation: Avoid storing private or confidential information and define explicit deletion, expiration, and approval procedures for persistent observations.

## Reference(s):

- [SKILL.md](SKILL.md)
- [Anti-Patterns](references/anti-patterns.md)
- [Reflection Levels](references/reflection-levels.md)
- [self-state.json Schema](references/self-state-schema.md)
- [SELF.md Template](references/self-template.md)
- [Trigger Model](references/trigger-model.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with configuration steps and a JSON state schema]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory guidance for SELF.md, HEARTBEAT.md, AGENTS.md, and memory/self-state.json.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
