## Description:

通过 Gecho Bridge MCP 发起异步 TikTok 商品、趋势、竞品与内容洞察任务，并查询任务状态。需要安装 Gecho Chrome 扩展、保持有效的 TikTok 登录会话，并配置 Gecho Bridge MCP 服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to start Gecho-powered TikTok insight jobs for product research, trend discovery, competitor analysis, content strategy, and market-opportunity review. The skill also guides users through required Gecho Bridge MCP, Chrome extension, and TikTok browser-session setup when those prerequisites are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Gecho's Chrome extension and MCP bridge operating with a logged-in TikTok browser session.

Mitigation: Install only after reviewing the Gecho extension and package provenance, and keep the browser session active only when you intend to run TikTok insight tasks.

Risk: Asynchronous insight jobs may save research results to a directory.

Mitigation: Use an intended writable save directory, review saved outputs before using them for decisions, and avoid placing sensitive files in the output location.

Risk: TikTok login walls, captchas, browser state, or network issues can cause jobs to fail or remain running.

Mitigation: Confirm that the Gecho extension is logged in, TikTok is logged in, and the TikTok tab is usable before starting a job; report tool errors without fabricating findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/tiktok-insight-zh-cn)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, job identifiers, status summaries, and saved-result paths when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start asynchronous research jobs through Gecho MCP tools and may report a jobId, running/error/completed status, and saved output directory.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
