## Description:

OpenClaw Skill OS coordinates multiple skills, manages handoffs, and routes explicit orchestration requests to suitable skill combinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to coordinate multi-skill workflows, route explicit orchestration requests, and synthesize outputs across OpenClaw skill components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad default activation can interfere with predictable single-skill behavior.

Mitigation: Invoke the skill for explicit orchestration or multi-skill routing tasks, and narrow any always-active examples before deployment.

Risk: Routing and synthesis guidance can select an unsuitable skill combination or preserve too much context across handoffs.

Mitigation: Review routing decisions, keep handoff context limited to what each task requires, and validate outputs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/skill-os)
- [System architecture](artifact/docs/architecture.md)
- [Skill design best practices](artifact/docs/best-practices.md)
- [Troubleshooting guide](artifact/docs/troubleshooting.md)
- [Skill validator](artifact/tests/skill-validator.md)
- [Test case library](artifact/tests/test-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with routing plans, checklists, and occasional configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external binaries are required; output depends on the active skill set and user-provided task context.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact README lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
