## Description: <br>
小红书自动化运营工具，支持搜索笔记、查看笔记详情及评论、浏览推荐流、发布图文笔记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research Xiaohongshu/RedNote content, inspect note details and comments, browse recommendation feeds, and publish image-text notes through a locally managed MCP component. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates platform actions to a separately installed third-party Xiaohongshu MCP component. <br>
Mitigation: Review and pin the third-party component before use, keep it bound to localhost, and use the setup checklist before installation. <br>
Risk: Publish actions can create public content that may be difficult or impossible to fully reverse. <br>
Mitigation: Use a dedicated Xiaohongshu account, require explicit per-post authorization, and rely on the client guardrails that block non-interactive publishing without --yes and XHS_DEDICATED_ACCOUNT=yes. <br>
Risk: Connecting to a remote MCP endpoint could expose account actions beyond the user's local machine. <br>
Mitigation: The client defaults to localhost and rejects non-loopback endpoints unless the user explicitly overrides that behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wscats/xhs-cn) <br>
- [Setup guide](SETUP.md) <br>
- [Third-party xiaohongshu-mcp component](https://github.com/xpzouying/xiaohongshu-mcp) <br>
- [Third-party xiaohongshu-mcp releases](https://github.com/xpzouying/xiaohongshu-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON responses from the local client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publish actions require explicit user authorization and client-side guardrails for loopback endpoints, non-interactive execution, and dedicated account declaration.] <br>

## Skill Version(s): <br>
1.0.10 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
