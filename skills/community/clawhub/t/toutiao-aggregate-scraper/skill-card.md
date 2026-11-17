## Description:

今日头条数据查询助手。覆盖文章、视频、用户、评论等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and media or content teams use this skill to query Toutiao articles, videos, users, and comments through MaxHub APIs and produce concise browse, analysis, comparison, or monitoring results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a MaxHub API key and sends Toutiao-related IDs, URLs, and queries to www.aconfig.cn.

Mitigation: Use it only when this data sharing is acceptable, and keep MAXHUB_API_KEY configured as a sensitive secret.

Risk: The skill includes fallback guidance to unrelated non-Toutiao platform endpoints.

Mitigation: Review or remove that fallback guidance before deployment and constrain calls to documented Toutiao endpoints.

Risk: An unpinned installer command may resolve to a changed package later.

Mitigation: Prefer a pinned or otherwise verified ClawHub installation path for production use.

## Reference(s):

- [Content & User API](references/api-content-user.md)
- [Parameter Mappings](references/param-mappings.md)
- [MaxHub Website](https://www.aconfig.cn)
- [ClawHub Skill Page](https://clawhub.ai/new-ironman/skills/toutiao-aggregate-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with tables, bullet points, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese or English responses; API key values are not shown in output.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
