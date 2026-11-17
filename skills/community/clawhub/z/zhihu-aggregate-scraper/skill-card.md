## Description:

知乎数据查询助手。覆盖用户信息、搜索、专栏、问答、热榜、评论等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, content teams, and brand teams use this skill to query and analyze Zhihu users, searches, trending topics, columns, answers, articles, and comments through MaxHub API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Zhihu queries, user IDs, and the configured API key to MaxHub and aconfig.cn.

Mitigation: Use it only when you trust MaxHub and aconfig.cn with that data, and keep API key values out of prompts and outputs.

Risk: Server security review reports scope and disclosure issues, including unrelated Douyin/Xiaohongshu fallback material.

Mitigation: Review before installation, narrow activation rules, remove unrelated fallback material, and add a clear privacy disclosure.

Risk: Some API behavior may involve live session tokens.

Mitigation: Avoid providing live session tokens unless the operator has reviewed the endpoint behavior and accepts the account and privacy risk.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/new-ironman/skills/zhihu-aggregate-scraper)
- [MaxHub API Website](https://www.aconfig.cn)
- [User Data API](artifact/references/api-user.md)
- [Search & Trending API](artifact/references/api-search-trending.md)
- [Content API](artifact/references/api-content.md)
- [Parameter Mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, bullet points, links, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English/Chinese responses; API key values should stay out of outputs.]

## Skill Version(s):

3.6.1 (source: server release, metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
