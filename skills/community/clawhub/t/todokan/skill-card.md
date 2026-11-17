## Description:

Manage tasks, boards, thoughts, and reviews in Todokan via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banatealab](https://clawhub.ai/user/banatealab)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect agents to Todokan for task, board, document, comment, and review workflows through MCP. It supports reading task state, preparing task or document drafts, and performing confirmed updates through the configured Todokan endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents an override that can expose tasks not marked as visible to AI.

Mitigation: Review AI visibility behavior before installation and avoid enabling workflows that query non-AI tasks unless that access is intentional.

Risk: Planner endpoint access can create, update, or delete Todokan data.

Mitigation: Use the worker endpoint for least privilege when read and comment access is sufficient, and require explicit confirmation before destructive actions.

Risk: Task titles, descriptions, comments, or documents may contain secrets or sensitive personal data.

Mitigation: Avoid placing secrets or sensitive personal data in Todokan tasks, and warn users before storing sensitive content.

## Reference(s):

- [Todokan homepage](https://todokan.com)
- [Todokan ClawHub skill page](https://clawhub.ai/banatealab/skills/todokan)
- [OpenClaw MCP documentation](https://openclaw.dev/docs/mcp)

## Skill Output:

**Output Type(s):** [Markdown, Text, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with task drafts, briefings, document drafts, and MCP tool call instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Todokan MCP endpoints configured with TODOKAN_API_KEY and TODOKAN_MCP_URL.]

## Skill Version(s):

1.3.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
