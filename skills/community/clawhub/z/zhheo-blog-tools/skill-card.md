## Description:

通过 HTTP API 访问张洪Heo博客：全文搜索、热门文章、归档浏览、标签分类、页面发现、友链查询、读文摘要。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhheo](https://clawhub.ai/user/zhheo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search, browse, summarize, and cite content from the Zhang Hong Heo blog through documented HTTP API endpoints without opening a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger words can cause the skill to activate for general blog-related prompts.

Mitigation: Consider narrowing triggers during installation if accidental activation would be disruptive.

Risk: The skill may call blog.zhheo.com when matching prompts request searches, hot articles, archives, tags, pages, friend links, or article content.

Mitigation: Review outbound HTTP access expectations before deployment in restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhheo/skills/zhheo-blog-tools)
- [Zhang Hong Heo blog](https://blog.zhheo.com)
- [Blog search API](https://blog.zhheo.com/api/search/search.php?q=OpenClaw&limit=5)
- [Blog hot articles API](https://blog.zhheo.com/api/umami/hot.php?period=day&limit=5)
- [Blog equipment page](https://blog.zhheo.com/equipment/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text responses with HTTP API paths, URLs, summaries, and occasional curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should preserve API-returned paths and note truncation when article text exceeds the documented length limit.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
