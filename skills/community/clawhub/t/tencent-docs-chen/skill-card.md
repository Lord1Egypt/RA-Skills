## Description:

Tencent Docs provides complete Tencent Docs operations for creating, reading, editing, and managing online documents, spreadsheets, slides, mind maps, flowcharts, knowledge base spaces, and space nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Tencent Docs for cloud document creation, content retrieval, editing, file management, and structured spreadsheet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise broad control over a Tencent Docs account, including creating, reading, editing, exporting, moving, and deleting documents.

Mitigation: Install it only for accounts where this access is acceptable, and review requested document operations before execution.

Risk: Credential handling depends on a Tencent Docs token passed through TENCENT_DOCS_TOKEN and an Authorization header.

Mitigation: Provide the token through the environment, avoid pasting raw tokens or cookies into prompts or scripts, and rotate the token if it is exposed.

Risk: Delete and bulk update tools can remove or overwrite Tencent Docs content.

Mitigation: Require explicit confirmation before delete, recursive delete, or bulk update actions, and verify target file, node, sheet, field, and record IDs.

Risk: URL scraping can send webpage content to Tencent Docs and store it as a cloud document.

Mitigation: Scrape only URLs the user intentionally wants transferred and stored, and confirm sensitivity and destination before starting the scrape task.

Risk: The setup script installs or uses the mcporter dependency to register the Tencent Docs MCP service.

Mitigation: Review or pin mcporter in managed environments before running setup.

## Reference(s):

- [Tencent Docs Skill Page](https://clawhub.ai/jason-aka-chen/skills/tencent-docs-chen)
- [Tencent Docs Homepage](https://docs.qq.com/home)
- [Tencent Docs MCP Token](https://docs.qq.com/open/document/mcp/get-token/)
- [Tencent Docs OpenClaw Token Guide](https://docs.qq.com/scenario/open-claw.html)
- [API Reference](references/api_references.md)
- [Management Reference](references/manage_references.md)
- [Sheet Reference](references/sheet_references.md)
- [SmartCanvas Reference](references/smartcanvas_references.md)
- [SmartSheet Reference](references/smartsheet_references.md)
- [Word Document Entry Guide](doc/entry.md)
- [Document Formatting Guide](doc/doc_format/README.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Tencent Docs token configured as TENCENT_DOCS_TOKEN and uses mcporter to call the Tencent Docs MCP service.]

## Skill Version(s):

1.0.11 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
