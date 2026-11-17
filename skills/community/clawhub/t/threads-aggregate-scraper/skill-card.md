## Description:

Threads 数据查询助手。覆盖帖子详情、用户资料、搜索、评论、转发等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Threads posts, user profiles, search results, comments, and repost-related data through MaxHub read-only APIs for social media monitoring and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user queries and URLs to a third-party MaxHub API and requires a sensitive API key.

Mitigation: Avoid sensitive or private query content, verify the MaxHub provider before use, and keep MAXHUB_API_KEY out of prompts, logs, and responses.

Risk: The security review flags broader activation and platform scope than the stated Threads-only purpose.

Mitigation: Use the skill only for intended Threads lookups and remove or split unrelated Douyin/Xiaohongshu references before broad deployment.

Risk: Server-resolved import provenance is unavailable for this version.

Mitigation: Install only from a trusted ClawHub source and prefer a pinned or otherwise trusted installer command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/threads-aggregate-scraper)
- [MaxHub website](https://www.aconfig.cn)
- [Post & User API reference](artifact/references/api-post-user.md)
- [Parameter mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with API query summaries, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual English or Chinese output, API result summaries, analysis, comparisons, and next-step guidance while keeping API keys out of responses.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
