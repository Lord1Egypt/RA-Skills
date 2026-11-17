## Description:

通过 Gecho Bridge MCP 采集 TikTok 创作者的公开视频，返回视频元数据、文案、互动指标、发布时间和链接。需要安装 Gecho Chrome 扩展、保持有效的 TikTok 登录会话，并配置 Gecho Bridge MCP 服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect and summarize public TikTok creator video metadata through the Gecho Bridge MCP workflow. It supports creator research by returning concise summaries, result counts, saved-file paths when available, and selected video fields rather than full raw JSON in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a logged-in Chrome browser session and a Gecho Chrome extension connected to TikTok.

Mitigation: Install only if that browser-session access is acceptable, keep unrelated sensitive accounts out of the active browser session, and resolve login, CAPTCHA, region, or cookie prompts manually before use.

Risk: Setup commands install the Gecho Bridge package with the latest npm release, which can reduce install reproducibility.

Mitigation: Review commands before running them and pin the Gecho Bridge package version when reproducible deployment is required.

Risk: TikTok pages may return no data or become blocked by platform checks, and the skill must not fabricate or retry through unofficial scraping routes.

Mitigation: Stop on empty or failed tool results, report the exact failure, and use only the official Gecho MCP workflow described by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/tiktok-influencer-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw + TikTok configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes + TikTok configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and concise summaries of JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a local saved-file path and selected fields from the first 3 to 5 collected TikTok videos; avoids pasting full raw JSON into chat.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
