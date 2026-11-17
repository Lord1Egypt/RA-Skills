## Description:

小红书全场景数据查询助手，支持 App 和 Web 多版本 API，用于查询笔记详情、用户数据、搜索结果、商品、评论和话题数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketing teams, product teams, and developers use this skill to collect and analyze Xiaohongshu notes, comments, user profiles, products, topics, KOL candidates, and consumer-trend signals through MaxHub APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some Xiaohongshu endpoints can send sensitive session cookies or proxy credentials to a third-party API service.

Mitigation: Use only accounts and credentials appropriate for MaxHub/aconfig.cn, prefer test accounts when possible, and rotate or revoke cookies and proxy credentials after use.

Risk: The security scan verdict is suspicious because the skill depends on a third-party data API and credential-bearing requests.

Mitigation: Install only after reviewing the provider trust boundary, required MAXHUB_API_KEY, and network access to https://www.aconfig.cn.

Risk: Mutable installer commands can change what is installed over time.

Mitigation: Prefer a pinned or otherwise verified installer before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/new-ironman/skills/xiaohongshu-aggregate-scraper)
- [MaxHub API Website](https://www.aconfig.cn)
- [README](README.md)
- [Chinese README](README_CN.md)
- [Note Data API](references/api-note.md)
- [User Data API](references/api-user.md)
- [Search API](references/api-search.md)
- [Product & Topic API](references/api-product-topic.md)
- [Parameter Mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese or English responses, with API keys omitted from output.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
