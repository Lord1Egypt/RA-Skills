## Description:

Xiaobai Workflow Enforcer guides AI agents through mandatory design, planning, test-first, execution, and verification gates for coding work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make an AI coding agent pause for design, planning, test-first implementation, checkpoint updates, and final verification before claiming completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can slow normal coding work by enforcing design, planning, test-first, and verification gates.

Mitigation: Install it only when those workflow gates are desired, and apply proportional exceptions for small or urgent tasks.

Risk: The skill can cause extra approvals or refusals when plans, tests, or verification evidence are missing.

Mitigation: Make user-instruction precedence explicit and review any refusal or delay against the current task requirements.

Risk: The skill can lead an agent to create design or checkpoint files in the workspace.

Mitigation: Review generated workspace files before committing or relying on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with workflow checklists and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead the agent to create design and checkpoint files as part of enforced workflow tracking.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
