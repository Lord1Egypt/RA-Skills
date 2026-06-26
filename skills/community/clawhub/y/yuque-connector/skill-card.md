## Description: <br>
语雀知识库双向同步技能，支持将本地 Word、Excel、Markdown、HTML、文本和 zip 文件导入语雀，也支持将语雀文档下载为本地 Markdown 文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuwu2495](https://clawhub.ai/user/jiuwu2495) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and external users with Yuque accounts use this skill to move documents between local files and Yuque knowledge bases. It supports bulk import, document download, search, directory management, update workflows, and synchronization checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests a Yuque token with read and write account access. <br>
Mitigation: Use the least-privileged token Yuque supports, avoid pasting long-lived secrets into ordinary chat, and rotate the token if it may have been exposed. <br>
Risk: The skill can modify local MCP configuration. <br>
Mitigation: Review any ~/.workbuddy/mcp.json change before applying it and keep the generated backup for rollback. <br>
Risk: Bulk synchronization can create, update, or download many documents at once. <br>
Mitigation: Confirm target knowledge bases and document lists before bulk operations, and keep local or Yuque backups when replacing existing content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiuwu2495/yuque-connector) <br>
- [Publisher profile](https://clawhub.ai/user/jiuwu2495) <br>
- [yuque-mcp server repository](https://github.com/yuque/yuque-mcp-server) <br>
- [Yuque API base](https://www.yuque.com/api/v2) <br>
- [Yuque token settings](https://www.yuque.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown responses, Yuque document links, local Markdown files, JSON configuration snippets, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Yuque documents, download Yuque content to local files, and modify local MCP configuration when the user configures the connector.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
