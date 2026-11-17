## Description:

Reddit data query assistant for posts, subreddits, users, search, comments, and feeds through MaxHub APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, researchers, content teams, and developers use this skill to collect and summarize Reddit posts, subreddit feeds, user profiles, search results, and comments for community monitoring, market research, and content discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires the sensitive MAXHUB_API_KEY credential for MaxHub API calls.

Mitigation: Keep the key out of logs and prompts, use a pinned and verified installer version, and only configure the credential in the intended runtime environment.

Risk: Security evidence reports non-Reddit fallback endpoint instructions despite the skill presenting itself as Reddit-only.

Mitigation: Before deployment, remove or ignore non-Reddit fallback instructions and allow only expected calls to https://www.aconfig.cn/api/v1/reddit/*.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/reddit-aggregate-scraper)
- [MaxHub API website](https://www.aconfig.cn)
- [Post Data API / 帖子数据接口](references/api-post.md)
- [Subreddit API / 版块接口](references/api-subreddit.md)
- [User & Search API / 用户与搜索接口](references/api-user-search.md)
- [Parameter Mappings / 参数映射](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with API-call guidance, summaries, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese output; uses MAXHUB_API_KEY for read-only MaxHub API calls.]

## Skill Version(s):

3.6.1 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
