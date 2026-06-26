## Description: <br>
UUMuse Brain helps an agent access, search, answer from, manage, and persist information in a user's UUMuse workspaces and knowledge bases through MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coding-today](https://clawhub.ai/user/coding-today) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent answer questions from their UUMuse documents, search uploaded knowledge bases, list workspace files, and manage cross-session memory. It is suited to document-backed assistance where the user has configured a UUMuse API key and MCP server access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad remote access to private UUMuse documents, workspaces, and long-term memory. <br>
Mitigation: Install only for trusted workspaces, use the narrowest available API key permissions, and treat search and answer results as access to private user data. <br>
Risk: Upload, overwrite, append, delete, remember, and forget operations can change or remove knowledge-base data. <br>
Mitigation: Require explicit user confirmation before write or destructive actions, especially in shared or business-critical workspaces. <br>
Risk: The configured MCP server runs through an external npm package or HTTP bridge and requires sensitive credentials. <br>
Mitigation: Use a trusted MCP package source, keep API keys out of logs and prompts, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [UUMuse](https://uumuse.ai) <br>
- [UUMuse API Docs](https://uumuse.ai/docs) <br>
- [uumuse-mcp on npm](https://www.npmjs.com/package/uumuse-mcp) <br>
- [UUMuse MCP GitHub Repository](https://github.com/UUMuse/uumuse-mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/coding-today/uumuse-brain) <br>
- [Publisher Profile](https://clawhub.ai/user/coding-today) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline commands, JSON configuration examples, and MCP tool responses with source citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a UUMuse API key and network access to the configured UUMuse MCP endpoint; some answer generation may consume UUMuse token balance.] <br>

## Skill Version(s): <br>
1.1.1 (source: server evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
