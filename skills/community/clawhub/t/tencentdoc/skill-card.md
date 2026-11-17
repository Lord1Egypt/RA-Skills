## Description:

Enables agents to create, read, edit, manage, import, export, and share Tencent Docs documents, sheets, slides, diagrams, spaces, and files through Tencent Docs MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmww](https://clawhub.ai/user/nmww)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Tencent Docs cloud documents from an agent workflow, including creating and editing documents, spreadsheets, slides, diagrams, smart sheets, forms, folders, and knowledge-space nodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify, share, delete, move, import, export, and bulk replace Tencent Docs resources.

Mitigation: Require explicit user confirmation for destructive, bulk, import/export, and public sharing actions before tool execution.

Risk: The setup flow handles Tencent Docs authorization tokens unsafely.

Mitigation: Keep the Tencent Docs token out of prompts, terminal transcripts, and support logs; rotate or revoke the token if exposure is suspected.

Risk: Agent workflows may access or transmit sensitive cloud document content through the user's Tencent Docs account.

Mitigation: Use the skill only for documents the user intends the agent to process, and avoid sensitive documents unless that access is required.

## Reference(s):

- [Tencent Docs Skill Page](https://clawhub.ai/nmww/skills/tencentdoc)
- [Tencent Docs Homepage](https://docs.qq.com/home)
- [Tencent Docs MCP Endpoint](https://docs.qq.com/openapi/mcp)
- [Authentication and Authorization](references/auth.md)
- [Common Workflows](references/workflows.md)
- [File Management Reference](references/manage_references.md)
- [Smartcanvas Entry](smartcanvas/entry.md)
- [Sheet Entry](sheet/entry.md)
- [Document Entry](doc/entry.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON arguments, shell commands, and Tencent Docs links or API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, import, export, share, move, or delete cloud-hosted Tencent Docs resources through the user's authorized account.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
