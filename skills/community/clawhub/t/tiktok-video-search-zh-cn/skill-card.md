## Description:

通过 Gecho Bridge MCP 按关键词搜索 TikTok 视频，返回视频元数据、创作者、互动指标和链接；需要 Gecho Chrome 扩展、有效的 TikTok 登录会话和 Gecho Bridge MCP 配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route TikTok keyword searches through Gecho Bridge MCP, collect video metadata, creator details, engagement signals, and links, and receive concise result summaries with saved JSON output when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Gecho's Chrome extension and MCP package having access to a logged-in TikTok browser session.

Mitigation: Install only if that trust boundary is acceptable, review the setup steps, and use a browser profile that does not contain sensitive TikTok data you do not want available to the integration.

Risk: Search execution can fail when Gecho Bridge, the Gecho extension, or the TikTok browser session is missing, disconnected, blocked by login, or blocked by CAPTCHA.

Mitigation: Confirm Gecho Bridge MCP is configured, the Gecho extension is logged in and online, and TikTok is open in Chrome before running a search; resolve login or CAPTCHA prompts manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/tiktok-video-search-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown responses with optional shell command blocks, summarized TikTok video metadata, JSON result references, and saved file paths when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the first 3 to 5 useful results and avoids pasting full raw JSON into chat.]

## Skill Version(s):

1.1.38 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
