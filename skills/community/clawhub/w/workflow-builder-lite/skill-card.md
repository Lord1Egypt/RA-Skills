## Description:

Build and execute multi-step workflows with conditional logic, chaining API calls, agent actions, and shell commands into reusable saved workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to define, save, review, and run reusable multi-step workflows with conditional branching while requiring confirmation for shell commands and file writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved workflows may later run shell commands, write files, call external APIs, or send messages.

Mitigation: Review saved workflows before running them and require explicit approval for shell commands and file writes.

Risk: Workflow automation can preserve actions that are no longer appropriate after context changes.

Mitigation: Show the workflow steps before execution and report progress after each step so the user can stop or revise the run.

## Reference(s):

- [Workflow Builder Lite on ClawHub](https://clawhub.ai/tommot2/skills/workflow-builder-lite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown workflow plans, progress updates, and reusable workflow files with optional shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shell command and file-write steps require per-step user confirmation.]

## Skill Version(s):

2.0.0 (source: server evidence and skill heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
