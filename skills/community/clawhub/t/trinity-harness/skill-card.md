## Description:

Production-grade Agent Harness combining execution discipline, knowledge compounding, and product thinking into a single adaptive workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[christianye](https://clawhub.ai/user/christianye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to structure feature work, bug fixes, reviews, debugging, and multi-step agent tasks with planning, verification, checkpointing, and review practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may route ordinary build, plan, review, ship, or debug requests through this workflow more often than desired.

Mitigation: Review and narrow the activation terms before deployment if the intended routing scope is smaller.

Risk: The workflow encourages agents to run verification commands, write checkpoint or output files, and use limited subagents for larger tasks.

Mitigation: Deploy in an environment with normal command, filesystem, and delegation controls, and review proposed actions before execution.

## Reference(s):

- [Checkpoint Patterns for Agent Systems](references/checkpoint-patterns.md)
- [MAST Failure Taxonomy for Multi-Agent Systems](references/mast-failure-taxonomy.md)
- [ClawHub Skill Page](https://clawhub.ai/christianye/skills/trinity-harness)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline checklists, tables, command examples, and workflow rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable payload; the skill steers agent behavior and generated work products.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
