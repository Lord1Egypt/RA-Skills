## Description: <br>
Uses the MCP protocol to operate the Toutiao platform for account management and content publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, knowledge sharers, and multi-platform operators use this skill to manage Toutiao login state and publish articles, micro posts, or Xiaohongshu-derived batches to Toutiao through a configured MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a saved Toutiao login to publish public content, including batch posts, through external code. <br>
Mitigation: Use a dedicated Toutiao account where possible, review the external toutiao-mcp server before installation, and require explicit preview and confirmation before every article, micro post, or batch publish. <br>
Risk: Saved cookies can grant continued access to the Toutiao account. <br>
Mitigation: Protect the cookie file path, restrict file permissions, and clear or rotate the cookie file when access should end. <br>
Risk: Remote image URLs and download directories used for publishing can introduce unwanted files or incorrect media into posts. <br>
Mitigation: Validate image URLs, local paths, and download directories before publishing, and keep downloaded assets in a dedicated working directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sipingme/toutiao-mcp-skill) <br>
- [Toutiao MCP Skill repository](https://github.com/sipingme/toutiao-mcp-skill) <br>
- [toutiao-mcp MCP server](https://github.com/sipingme/toutiao-mcp) <br>
- [Quick Start](references/quick-start.md) <br>
- [FAQ](references/faq.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON tool payloads] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON MCP tool examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public-content publishing instructions and MCP tool payloads for login, article publishing, micro posts, batch publishing, and logout.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
