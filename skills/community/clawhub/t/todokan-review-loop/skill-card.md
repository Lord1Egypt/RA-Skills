## Description:

Process Todokan task and thought boards with a review-loop workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banatealab](https://clawhub.ai/user/banatealab)

### License/Terms of Use:


## Use Case:

External users and teams use this skill to automate Todokan review-loop task handling: read AI-enabled doing tasks, understand the full comment thread, post concise context-aware updates, and move addressed tasks to done/Review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read enabled Todokan task context and comments.

Mitigation: Install it only for Todokan workspaces where AI-enabled task review is intended, and keep read scopes limited to the boards and tasks needed for the workflow.

Risk: The skill can post comments, attach task documents, and move addressed tasks to done/Review.

Mitigation: Configure write scopes narrowly, monitor review-loop runs, and rely on Todokan's done/Review state for human review before final closure.

Risk: The skill requires Todokan API credentials and MCP configuration.

Mitigation: Store TODOKAN_API_KEY securely, rotate it as needed, and avoid granting broader MCP permissions than the documented task and comment workflow requires.

## Reference(s):

- [Todokan](https://todokan.com)
- [Todokan MCP endpoint](https://todokan.com/mcp)
- [ClawHub skill page](https://clawhub.ai/banatealab/skills/todokan-review-loop)
- [ClawHub publisher profile](https://clawhub.ai/user/banatealab)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Concise Todokan comments, optional task documents, and status updates through the configured MCP server.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TODOKAN_API_KEY, TODOKAN_MCP_URL, and Todokan MCP access scoped for reading tasks/comments and writing comments/status updates.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
