## Description:

小红书自动化运营工具，支持搜索笔记、查看笔记详情及评论、浏览推荐流、发布图文笔记。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to research Xiaohongshu/RedNote notes, inspect comments and engagement, browse feeds, and publish image notes through a locally running, user-managed MCP component.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote endpoint override can expose tokens, searches, and draft posts outside the local machine.

Mitigation: Keep the MCP endpoint bound to localhost and do not set XHS_ALLOW_REMOTE=yes unless the endpoint and transport are fully trusted.

Risk: Publishing can create public Xiaohongshu content through the connected account.

Mitigation: Use a dedicated Xiaohongshu account and require per-post preview, explicit authorization, and the XHS_DEDICATED_ACCOUNT=yes declaration before publishing.

Risk: The skill depends on a separately installed third-party MCP component and Python dependency.

Mitigation: Pin and review the third-party component version and Python dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/xhs-mcp)
- [Publisher profile](https://clawhub.ai/user/wscats)
- [Third-party xiaohongshu-mcp component](https://github.com/xpzouying/xiaohongshu-mcp)
- [Third-party component releases](https://github.com/xpzouying/xiaohongshu-mcp/releases)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text and optional JSON responses, with Markdown workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Xiaohongshu MCP server; publishing is gated by explicit confirmation and a dedicated-account declaration.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
