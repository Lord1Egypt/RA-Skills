## Description:

Search and read the owner's chosen Google Drive folders offline through drive — Docs, Sheets, PDF and docx as local text, with tags, notes, memories and editors. Use when a question needs what a Drive document says, who changed it, or to note or tag one; not for files outside the imported folders or for editing documents unless asked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to search and read documents from their imported Google Drive folders, answer questions about document contents or edit history, and add local tags or notes when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory extraction sends document text to the user's configured model.

Mitigation: Run memory extraction only on a document the owner has named, and use the intended configured model.

Risk: Write access or MCP serving can expose document-changing capabilities.

Mitigation: Use read-only mode for search and reading; enable write access or MCP serving only when needed, and make Drive changes only when the owner requests them.

## Reference(s):

- [Drive Cli on ClawHub](https://clawhub.ai/wirecat/skills/wirecat-drive)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Natural-language responses with document links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited to imported folders and depend on the user's request and available Drive permissions.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
