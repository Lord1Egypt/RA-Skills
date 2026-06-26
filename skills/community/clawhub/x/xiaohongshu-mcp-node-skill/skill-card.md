## Description: <br>
通过 MCP 协议操作小红书平台，支持内容发布、搜索、互动等完整功能 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an agent to a Xiaohongshu MCP server for account login, publishing posts or videos, searching content, reading details, and performing user-approved interactions such as comments, likes, and favorites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real Xiaohongshu account through an external MCP server and browser automation. <br>
Mitigation: Use only with accounts and actions the user explicitly authorizes, and require manual confirmation before publishing, commenting, liking, favoriting, or changing visibility. <br>
Risk: Reusable login cookies are stored locally and could allow account access if exposed. <br>
Mitigation: Store `cookies.json` outside shared directories and protect it with restrictive file permissions such as `chmod 600`. <br>
Risk: The quick-start documentation recommends a remote `curl | bash` installer. <br>
Mitigation: Inspect, pin, or manually install the repository before running installation commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sipingme/xiaohongshu-mcp-node-skill) <br>
- [Project GitHub](https://github.com/sipingme/xiaohongshu-mcp-node-skill) <br>
- [xiaohongshu-mcp-node core library](https://github.com/sipingme/xiaohongshu-mcp-node) <br>
- [Quick Start Guide](references/quick-start.md) <br>
- [FAQ](references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce command examples and user-facing workflow guidance for browser automation against a logged-in Xiaohongshu account.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
