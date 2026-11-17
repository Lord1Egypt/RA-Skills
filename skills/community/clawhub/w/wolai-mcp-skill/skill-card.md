## Description:

Wolai MCP skill for operating Wolai notes, including blocks, pages, search, and database workflows through the MCP protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cizixiu](https://clawhub.ai/user/cizixiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Wolai users use this skill to let an agent read, search, create, update, and delete Wolai pages and blocks through Wolai's MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expose their Wolai access token in chat while trying to configure the skill.

Mitigation: Configure WOLAI_MCP_TOKEN manually through the operating system environment or a secure secret store, and revoke any token that was shared in chat.

Risk: A valid Wolai token can give the assistant-driven workflow broad access to read, write, delete, and permanently delete Wolai notes.

Mitigation: Use the narrowest Wolai token available, review requested operations before execution, and avoid permanent delete operations unless explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cizixiu/skills/wolai-mcp-skill)
- [Publisher profile](https://clawhub.ai/user/cizixiu)
- [Wolai](https://www.wolai.com)
- [Wolai MCP endpoint](https://api.wolai.com/v1/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided WOLAI_MCP_TOKEN environment variable for Wolai API access.]

## Skill Version(s):

1.3.4 (source: server release metadata; artifact frontmatter reports 1.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
