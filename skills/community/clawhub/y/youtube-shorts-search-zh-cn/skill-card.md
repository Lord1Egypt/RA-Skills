## Description:

通过官方 Gecho Bridge MCP 按关键词搜索 YouTube Shorts，返回排序后的视频、互动数据、详情、评论和链接。用户需要 YouTube Shorts 调研或监测时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, social media researchers, and developers use this skill to route YouTube Shorts keyword searches through Gecho Bridge MCP and summarize sorted video records, engagement data, details, comments, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Gecho's MCP package, Chrome extension, and a logged-in browser session.

Mitigation: Before installing or running it, confirm that the user trusts Gecho's MCP package and Chrome extension and understands that the workflow uses their active browser session.

Risk: YouTube login, captcha, verification, region, cookie, timeout, or extension-connection issues can block or partially complete collection.

Mitigation: Ask the user to resolve browser prompts manually in Chrome, stop on tool errors or timeouts, and clearly report empty, partial, or failed results.

Risk: Installing only the skill does not make the YouTube Shorts collection workflow executable.

Mitigation: Provide the documented Gecho Bridge MCP setup steps and required Chrome extension and login prerequisites when the MCP tool is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/youtube-shorts-search-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge GitHub repository](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- [Gecho YouTube channel](https://www.youtube.com/@Gecho-AI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with structured video summaries, links, configuration commands, and status or error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include up to 20 sorted YouTube Shorts records when the Gecho MCP workflow succeeds, plus a local save path when available.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
