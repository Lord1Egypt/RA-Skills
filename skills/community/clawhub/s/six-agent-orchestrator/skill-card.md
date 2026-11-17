## Description:

Six Agent Orchestrator is a Chinese-language workflow template that defines six agent roles, a six-stage task pipeline, token quota monitoring, and role-boundary checks for coordinating software tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xb19960921](https://clawhub.ai/user/xb19960921)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill as a Chinese-language coordination template for breaking coding tasks into planning, execution, verification, fixing, and summary stages with named agent responsibilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on the skill as if it automatically spawns independent agents or enforces safety boundaries.

Mitigation: Treat the role and red-line sections as workflow guidance unless the deployment environment independently implements and tests those controls.

Risk: Users may assume token quotas are automatically enforced across model providers.

Mitigation: Verify quota tracking in the target runtime and add provider-level limits or monitoring before using it for cost-sensitive work.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and optional Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes JSON configuration files and Python helper scripts; token usage and red-line checks should be treated as advisory unless independently enforced.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
