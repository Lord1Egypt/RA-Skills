## Description:

通过官方 Gecho Bridge MCP 获取一条 X（Twitter）帖子及其回复。用户提供 X 帖子 URL，并需要正文、作者、互动数据或评论时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social-media researchers use this skill to retrieve one known X/Twitter post, its author details, engagement data, and available replies through the official Gecho workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses a logged-in Chrome session and can access X content visible to that session.

Mitigation: Use it only with browser sessions and X accounts approved for the task, and review the target URL before running the workflow.

Risk: Missing Gecho Bridge, the Chrome extension, X login, or manual resolution of platform prompts can cause failed or incomplete retrieval.

Mitigation: Confirm the required Gecho Bridge service, extension login, X login, and any platform prompts before asking the agent to run the skill.

Risk: The skill depends on the official Gecho MCP workflow and should not be replaced by ad hoc scraping or browser automation.

Mitigation: Use only the documented Gecho MCP tool for this workflow and stop on tool errors, empty results, or timeouts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/x-post-detail-zh-cn)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho website](https://gecho.ai/)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw configuration video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes configuration video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with configuration commands and saved-result paths when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes the most useful 3 to 5 returned fields or replies and avoids pasting full raw JSON into chat.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
