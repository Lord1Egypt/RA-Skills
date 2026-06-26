## Description: <br>
Coordinate multiple agents and tasks for complex workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobisamaa](https://clawhub.ai/user/tobisamaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to plan and coordinate complex multi-step workflows across multiple agents, including dependency management, parallel execution, supervision, and result aggregation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate broad multi-agent actions, including spawning, steering, killing, publishing, deploying, and writing shared workflow files. <br>
Mitigation: Require explicit user approval before any high-impact orchestration action and review proposed workflow changes before execution. <br>
Risk: Shared workflow state can expose secrets or private data to multiple agents. <br>
Mitigation: Avoid placing secrets or private data in shared state, and scope agent instructions to only the data required for the task. <br>
Risk: The evidence reports unexplained requirements for BRAVE_API_KEY and the npm async package. <br>
Mitigation: Ask the publisher why those requirements are needed before granting the environment variable or installing the package. <br>


## Reference(s): <br>
- [Task Orchestra on ClawHub](https://clawhub.ai/tobisamaa/task-orchestra) <br>
- [Publisher profile](https://clawhub.ai/user/tobisamaa) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with workflow outlines and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose subagent orchestration, dependency ordering, retry strategies, and shared workflow state.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
