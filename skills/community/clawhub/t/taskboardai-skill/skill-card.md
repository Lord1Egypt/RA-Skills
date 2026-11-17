## Description:

Manage tasks and projects using the TaskBoardAI Kanban system. Includes MCP server integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyddd](https://clawhub.ai/user/hyddd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create, update, block, and complete TaskBoardAI Kanban tasks through an MCP-backed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist task details and final results to TaskBoardAI, which may include sensitive context.

Mitigation: Use explicit user confirmation before task creation and store sanitized summaries instead of full conversation context.

Risk: The setup uses a global TaskBoardAI dependency without a pinned version.

Mitigation: Pin and verify the TaskBoardAI package version before installation or deployment.

Risk: The MCP server may have access to local filesystem or environment data depending on how it is launched.

Mitigation: Run the MCP server with restricted filesystem and environment access appropriate to the deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hyddd/skills/taskboardai-skill)
- [TaskBoardAI Project](https://github.com/taskboardai/taskboardai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured task updates with inline shell commands or configuration snippets when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update TaskBoardAI task content and status through the configured MCP server.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
