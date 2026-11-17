## Description:

Short interview to surface the real goal behind an ambiguous request before executing - Karpathy layer 1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanbastias](https://clawhub.ai/user/juanbastias)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to clarify ambiguous or broad requests before work begins. It guides the agent through a short interview, converts answers into a reusable objective spec, and waits for confirmation before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add extra clarification turns before execution.

Mitigation: Use it for ambiguous or broad requests where a short interview costs less than acting on the wrong objective.

Risk: A saved or reused objective spec may contain user goals, constraints, or success criteria.

Mitigation: Review the spec before reuse and avoid storing sensitive details unless the project context requires them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/juanbastias/skills/real-objective-discovery)
- [ClawHub publisher profile](https://clawhub.ai/user/juanbastias)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown conversation prompts and a short objective spec]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask up to three clarification questions before producing and confirming a reusable spec.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
