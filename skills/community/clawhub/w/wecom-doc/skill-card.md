## Description:

Creates and edits WeCom documents and smart sheets through a configured MCP server, including document creation, content writing, sheet setup, field updates, and record insertion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garfileds](https://clawhub.ai/user/garfileds)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents in WeCom/OpenClaw environments use this skill to create documents and smart sheets, then write document content or add sheets, fields, and records through the wecom-doc MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can install the global mcporter npm package.

Mitigation: Install only when the package and execution environment are trusted.

Risk: Setup can configure remote MCP endpoints from local or user-provided values.

Mitigation: Verify MCP URLs or JSON configuration before allowing future document actions to use that server.

Risk: Document content edits can perform full overwrites.

Mitigation: Review existing content before replacement when preserving prior document text matters.

## Reference(s):

- [WeCom document API reference](artifact/references/doc-api.md)
- [ClawHub skill page](https://clawhub.ai/garfileds/skills/wecom-doc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON MCP arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured wecom-doc MCP endpoint and the mcporter binary.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
