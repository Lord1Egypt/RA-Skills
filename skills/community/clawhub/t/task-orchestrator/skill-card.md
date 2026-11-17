## Description:

Intelligent task management and execution coordination officer. Automatically generates task lists, intelligently decomposes complex tasks, matches AI agents, makes priority decisions, and monitors progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to turn complex goals into structured task plans, assign suitable agents, prioritize dependencies, and monitor execution progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest agent execution, web search, publishing, sending, deployment, or retry actions.

Mitigation: Require explicit user approval before carrying out suggested external, publishing, deployment, or retry actions.

Risk: The included scripts can create or update local task JSON files.

Mitigation: Review target file paths and generated task content before using the outputs in a live workflow.

## Reference(s):

- [Task Orchestrator ClawHub Page](https://clawhub.ai/openlark/skills/task-orchestrator)
- [Agent Matching Strategy](references/agent_matching.md)
- [Task Template Library](references/task_templates.md)
- [Workflow Patterns](references/workflow_patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON task files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local task JSON files through included Python scripts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
