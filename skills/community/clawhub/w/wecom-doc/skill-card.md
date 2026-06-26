## Description: <br>
Creates and edits WeCom documents and smart sheets through the wecom-doc MCP server, including document creation, full-content writes, sheet fields, and records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garfileds](https://clawhub.ai/user/garfileds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to create WeCom documents and smart sheets, edit documents created during the session, and add smart-sheet sheets, fields, and records through mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and modify real WeCom documents and smart sheets through the configured WeCom/MCP account. <br>
Mitigation: Install only when this behavior is intended, and be explicit about the target platform and workspace before allowing document operations. <br>
Risk: The skill routes ordinary document creation and editing requests to WeCom by default. <br>
Mitigation: Confirm that WeCom is the desired platform when a request is ambiguous or could affect another document system. <br>
Risk: The edit_doc_content operation replaces the whole document. <br>
Mitigation: Require manual confirmation before running edit_doc_content and preserve or review existing content before overwriting it. <br>
Risk: The skill installs and depends on the mcporter package. <br>
Mitigation: Verify the mcporter package before global installation and ensure the configured MCP server is trusted. <br>


## Reference(s): <br>
- [wecom-doc on ClawHub](https://clawhub.ai/garfileds/wecom-doc) <br>
- [WeCom document API reference](references/doc-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON mcporter responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses mcporter to configure and call the wecom-doc MCP server; edit_doc_content performs full-document replacement.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
