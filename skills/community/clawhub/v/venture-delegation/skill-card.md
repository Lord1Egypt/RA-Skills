## Description:

Guides an agent through venture evaluation, atomic task decomposition, model assignment, execution planning, automated evaluation, and learning capture for new opportunities, projects, or oversized tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and agent operators use this skill to evaluate raw ideas, break larger goals into independently testable work atoms, assign each atom to an appropriate model, and produce a delegation plan for execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated delegation plans may contain incorrect sequencing, model assignments, or evaluation checks.

Mitigation: Review DELEGATION_PLAN.md before execution and adjust tasks, dependencies, models, and eval commands as needed.

Risk: Local planning and learning files may retain sensitive project history if task descriptions include confidential context.

Mitigation: Avoid including secrets in task descriptions and periodically delete or audit .learnings/LEARNINGS.md in sensitive workspaces.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown plans, structured tables, prompts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local planning and learning files such as DELEGATION_PLAN.md and .learnings/LEARNINGS.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
