## Description: <br>
Reddit 数据查询助手，覆盖帖子详情、版块、用户、搜索、评论、推荐等全功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Reddit posts, subreddit feeds, user profiles, searches, comments, and recommendations through the MaxHub API, then summarize or analyze the returned community data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MaxHub API key and sends Reddit queries to the external aconfig.cn service. <br>
Mitigation: Install only when the user trusts MaxHub/aconfig.cn with the API key and submitted query terms; avoid private identifiers or sensitive investigation terms. <br>
Risk: Security evidence notes automatic fallback guidance to unrelated Douyin/Xiaohongshu APIs. <br>
Mitigation: Review or remove the unrelated fallback instructions before autonomous use, and constrain execution to the documented Reddit endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/new-ironman/reddit-aggregate-scraper) <br>
- [MaxHub API Website](https://www.aconfig.cn) <br>
- [Post Data API Reference](references/api-post.md) <br>
- [Subreddit API Reference](references/api-subreddit.md) <br>
- [User and Search API Reference](references/api-user-search.md) <br>
- [Parameter Mappings](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bilingual English or Chinese responses, tables, analysis summaries, setup guidance, and next-step suggestions.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
