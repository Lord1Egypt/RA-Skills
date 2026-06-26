## Description: <br>
Connects an agent to Wolai's MCP API so it can search, read, create, update, and delete Wolai notes, pages, blocks, and databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cizixiu](https://clawhub.ai/user/cizixiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an assistant operate their Wolai workspace through MCP. It supports note workflows such as searching pages, reading outlines or sections, creating pages and blocks, updating content, and deleting pages or blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Wolai MCP token could be exposed to chat or logs if copied into an assistant conversation. <br>
Mitigation: Configure WOLAI_MCP_TOKEN manually in the local environment or a secure credential store, and rotate the token if it may have been shared. <br>
Risk: The skill can perform destructive Wolai operations, including deletes. <br>
Mitigation: Confirm destructive operations, especially permanent deletes, before executing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cizixiu/wolai-mcp-skill) <br>
- [Wolai](https://www.wolai.com) <br>
- [Wolai MCP endpoint](https://api.wolai.com/v1/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with PowerShell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WOLAI_MCP_TOKEN to be configured outside chat; generated actions may read, create, update, or delete Wolai content.] <br>

## Skill Version(s): <br>
1.3.4 (source: server release metadata; artifact frontmatter reports 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
