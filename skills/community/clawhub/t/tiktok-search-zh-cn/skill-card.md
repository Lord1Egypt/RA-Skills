## Description:

通过 Gecho Bridge MCP 搜索 TikTok 视频、采集创作者视频、获取指定视频详情与评论，并开展商品、趋势、竞品与内容洞察。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, marketers, ecommerce researchers, and agents use this skill to route TikTok search, creator collection, video-detail collection, comments, trend, product, competitor, and content-insight requests through Gecho Bridge MCP. It also provides setup and troubleshooting guidance when Gecho Bridge, the Chrome extension, or logged-in TikTok and Gecho sessions are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a logged-in Chrome, Gecho, and TikTok browser session.

Mitigation: Use a deliberate browser profile and confirm the Gecho extension and TikTok session are active before running searches or insight tasks.

Risk: Collected TikTok metadata, comments, URLs, and insight results may be saved to local JSON files.

Mitigation: Use a dedicated save directory, avoid shared folders for sensitive work, and review or delete saved outputs after use.

Risk: TikTok pages may be blocked by login walls, captchas, private videos, deleted videos, or page failures.

Mitigation: Report the exact page or tool status, stop the workflow, and require the user to resolve access issues or provide a valid URL before retrying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/tiktok-search-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, structured summaries, saved-file paths, and asynchronous insight job IDs when returned by Gecho MCP tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize TikTok metadata, comments, replies, status results, and insight findings; full raw result sets may be saved as local JSON files by the Gecho MCP workflow.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
