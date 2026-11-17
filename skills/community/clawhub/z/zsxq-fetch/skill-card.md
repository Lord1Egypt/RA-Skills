## Description:

知识星球帖子抓取助手自动抓取指定知识星球的最新帖子，支持全部或仅精华筛选、通过帖子链接或 ID 获取单条帖子详情，并支持多星球配置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxiaoqiao](https://clawhub.ai/user/huxiaoqiao)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to retrieve, review, summarize, and search Knowledge Planet group content that their configured account is authorized to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An embedded or persisted Knowledge Planet token could expose account access if reused, logged, committed, or shared.

Mitigation: Remove and revoke any embedded token, require the user to provide their own token through a secure local secret or environment variable, and avoid storing cookie tokens in plaintext files.

Risk: Fetched group lists and posts can reveal private memberships or restricted community content.

Mitigation: Use only accounts and groups the user is authorized to access, and avoid pasting tokens, private posts, logs, screenshots, or raw outputs into shared channels.

## Reference(s):

- [Skill listing on ClawHub](https://clawhub.ai/huxiaoqiao/skills/zsxq-fetch)
- [Publisher profile on ClawHub](https://clawhub.ai/user/huxiaoqiao)
- [知识星球 API 参考](references/api-reference.md)
- [Knowledge Planet web app](https://wx.zsxq.com)
- [Knowledge Planet API base URL](https://api.zsxq.com/v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Chinese text or Markdown summaries, with JSON returned by helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 18 and a Knowledge Planet access token; topic text is truncated to 5000 characters per item.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
