## Description:

Roo Code AI programming assistant guidance for VS Code agent workflows, mode switching, and MCP integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand and configure Roo Code as a VS Code coding agent for multi-step development, debugging, project setup, custom modes, and MCP-enabled workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-authority coding-agent and MCP integrations can access local files, run commands, or call connected services beyond the user's intent.

Mitigation: Review tool permissions before use, restrict filesystem access to intended project paths, and approve file or command actions before applying them.

Risk: The MCP example uses unpinned npx packages and a GitHub token without detailed scope limits.

Mitigation: Verify package identities, pin exact reviewed versions, and use a dedicated GitHub token with minimal required scopes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangifonly/skills/roo-code)
- [Publisher profile](https://clawhub.ai/user/zhangifonly)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup guidance, mode descriptions, MCP configuration examples, and installation commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
