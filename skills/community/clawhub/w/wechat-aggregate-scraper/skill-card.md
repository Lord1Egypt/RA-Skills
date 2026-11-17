## Description:

微信数据查询助手。覆盖视频号和公众号两大模块，支持搜索、视频详情、评论、文章、用户等全功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, operations, and social-media analysis teams use this skill to query WeChat Channels and Official Account data through MaxHub, then browse, analyze, or compare content, engagement, articles, comments, users, and related metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated WeChat search terms, article links, share URLs, and the MaxHub API key are sent to www.aconfig.cn.

Mitigation: Use a dedicated, revocable API key and install only when this third-party data flow is acceptable.

Risk: Broad auto-invocation may cause the skill to run on requests that are not explicitly intended for WeChat data lookup.

Mitigation: Invoke the skill only for explicit WeChat-related requests and review planned API calls before execution.

Risk: Video download or decryption-related output may require extra review before use.

Mitigation: Be cautious with any video download or decryption output and confirm that usage is authorized and appropriate.

Risk: The documented install command uses an unpinned npx path.

Mitigation: Prefer a pinned or otherwise trusted installer path for production use.

## Reference(s):

- [MaxHub API service](https://www.aconfig.cn)
- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/wechat-aggregate-scraper)
- [Channels API / 视频号接口](references/api-channels.md)
- [Media Platform API / 公众号接口](references/api-mp.md)
- [Parameter Mappings / 参数映射](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with tables, bullet summaries, links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual Chinese or English output, humanized numeric formatting, and notes when API data is unavailable or access is limited.]

## Skill Version(s):

3.6.1 (source: server release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
