## Description: <br>
Provides Xiaohongshu account management, login checks, content publishing, feed search/detail lookup, comments and replies, user profile lookup, and local MCP server management through a Python CLI and MCP REST API client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-p5](https://clawhub.ai/user/cn-p5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, and social media operators use this skill to manage Xiaohongshu sessions and accounts, publish notes or videos, retrieve feed and user data, and perform comment interactions from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Xiaohongshu login cookies and uses xsec tokens for account actions. <br>
Mitigation: Treat user_cookies.json, cookies.json, and xsec tokens like passwords, keep them out of shared directories, and remove them when no longer needed. <br>
Risk: The skill can publish content and post or reply to comments on live Xiaohongshu accounts. <br>
Mitigation: Confirm the active account and review the exact content before running publish, comment, or reply commands. <br>
Risk: The skill can download and run a local MCP server binary from an upstream release source. <br>
Mitigation: Use only trusted release sources, review the downloaded server binary provenance, and run the service from an isolated working directory where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-p5/xiaohongshu-aio) <br>
- [Publisher profile](https://clawhub.ai/user/cn-p5) <br>
- [Upstream Xiaohongshu MCP project](https://github.com/xpzouying/xiaohongshu-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, configuration values, and API-oriented instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require XHS_MCP_BASE_URL, python, uv, a running Xiaohongshu MCP server, and Xiaohongshu login cookies for account-specific actions.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
