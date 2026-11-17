## Description:

Coordinate multiple agents and tasks for complex workflows. Orchestrate subagents, manage dependencies, handle parallel execution, and ensure successful completion of multi-step operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobisamaa](https://clawhub.ai/user/tobisamaa)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to coordinate complex, multi-step workflows across multiple agents, including parallel execution, dependency management, supervision, and recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires BRAVE_API_KEY, but the evidence does not explain why Brave access is needed.

Mitigation: Only provide BRAVE_API_KEY after confirming the workflow requires Brave access, and scope or rotate the credential according to local policy.

Risk: The skill installs the npm package async without version pinning, and the security summary says the dependency is not clearly needed.

Mitigation: Pin the npm dependency to a reviewed version or remove it before using the skill in environments with sensitive files or credentials.

Risk: The skill coordinates multiple subagents and can amplify incorrect instructions or failed intermediate results across a workflow.

Mitigation: Review generated task plans, cap concurrent agents, validate handoffs, and inspect aggregate results before acting on them.

## Reference(s):

- [Task Orchestra ClawHub release](https://clawhub.ai/tobisamaa/skills/task-orchestra)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline command examples and workflow templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces orchestration patterns, task plans, subagent coordination guidance, recovery strategies, and command examples.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
