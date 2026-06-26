## Description: <br>
Tencent Docs provides agent workflows for creating, reading, editing, importing, exporting, and managing Tencent Docs documents, spreadsheets, slides, knowledge spaces, and nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate Tencent Docs document creation, content retrieval, editing, spreadsheet operations, and knowledge-space management from an agent with a configured Tencent Docs token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, read, edit, import, export, and delete Tencent Docs cloud documents. <br>
Mitigation: Review requested document IDs, folder targets, delete operations, and bulk updates before allowing tool calls to run. <br>
Risk: Local or confidential content may be sent to Tencent Docs services during document creation, import, upload, or editing. <br>
Mitigation: Do not provide sensitive local files or confidential text unless the user and organization have approved that data transfer. <br>
Risk: The setup script may install mcporter globally and persist token-backed MCP configuration. <br>
Mitigation: Review setup.sh before installation and confirm that TENCENT_DOCS_TOKEN is scoped and stored according to local policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jason-aka-chen/tencent-docs-chen) <br>
- [Tencent Docs Homepage](https://docs.qq.com/home) <br>
- [Tencent Docs Token Setup](https://docs.qq.com/open/document/mcp/get-token/) <br>
- [Tencent Docs OpenClaw Token Guide](https://docs.qq.com/scenario/open-claw.html) <br>
- [API References](references/api_references.md) <br>
- [Manage References](references/manage_references.md) <br>
- [Sheet References](references/sheet_references.md) <br>
- [SmartCanvas References](references/smartcanvas_references.md) <br>
- [SmartSheet References](references/smartsheet_references.md) <br>
- [Word Document Entry Guide](doc/entry.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with mcporter shell commands, JSON arguments, and Tencent Docs URLs or file identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, edit, import, export, move, rename, or delete cloud documents through Tencent Docs MCP tools.] <br>

## Skill Version(s): <br>
1.0.11 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
