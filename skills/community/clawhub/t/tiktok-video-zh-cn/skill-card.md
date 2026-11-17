## Description:

通过官方 Gecho Bridge MCP 获取指定 TikTok 视频详情、评论和回复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route a known TikTok video URL to Gecho Bridge for video metadata, comment, and reply collection, then summarize representative results or save raw JSON when a directory is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on the Gecho Chrome extension, Gecho Bridge MCP package, and a logged-in TikTok browser session, which can expose session-scoped platform data to the configured toolchain.

Mitigation: Install and use the extension and MCP package only in environments where the Gecho toolchain is trusted, and review extension/package trust before use in sensitive environments.

Risk: TikTok login walls, verification prompts, private or deleted videos, regional restrictions, and page blockers can prevent complete or accurate collection.

Mitigation: Use the skill only with videos the user intends to analyze, resolve browser-side access prompts manually, and report unavailable or incomplete data instead of inferring missing details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/tiktok-video-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw + TikTok configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes + TikTok configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summarized TikTok video/comment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a local JSON result file path when the Gecho tool saves raw output; comment and reply counts are limited by the live TikTok browser session and the tool cap.]

## Skill Version(s):

1.1.38 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
