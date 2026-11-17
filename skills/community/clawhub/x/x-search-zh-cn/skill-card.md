## Description:

通过官方 Gecho Bridge MCP 按关键词搜索公开的 X（Twitter）帖子，返回帖子文本、作者、互动数据和链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to route X (Twitter) keyword research or monitoring requests through the Gecho Bridge MCP workflow and receive concise summaries, links, and optional saved results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Gecho Bridge, a Chrome extension, and a logged-in X/Twitter browser session.

Mitigation: Confirm the MCP package and extension vendor before use, keep the browser session under user control, and manually resolve login, verification, region, or cookie prompts in Chrome.

Risk: Search results may be saved locally and can contain collected public post text, author metadata, engagement counts, and links.

Mitigation: Choose only save directories appropriate for the sensitivity of the research task and avoid storing results where unintended users can access them.

Risk: The skill should not bypass platform controls or substitute unofficial scraping methods.

Mitigation: Use only the official Gecho MCP x_search workflow and stop on missing tools, verification barriers, timeouts, or tool errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/x-search-zh-cn)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge GitHub repository](https://github.com/gecho-ai/gecho-bridge)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and concise search-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report result counts, the most useful 3 to 5 result fields, links, and a saved result path when available.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
