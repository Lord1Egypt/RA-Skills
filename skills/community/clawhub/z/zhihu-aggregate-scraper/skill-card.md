## Description: <br>
知乎数据查询助手。覆盖用户信息、搜索、专栏、问答、热榜、评论等全功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Zhihu user profiles, search results, trending content, articles, columns, questions, answers, and comments through MaxHub APIs for research, content planning, and reputation monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Zhihu search terms, user IDs, article IDs, comment IDs, and optional session tokens to MaxHub at www.aconfig.cn. <br>
Mitigation: Use only data that is appropriate to share with the third-party API provider, avoid private session tokens unless required and understood, and do not include sensitive personal data in queries. <br>
Risk: Security evidence flags non-Zhihu fallback instructions and weak guidance for sensitive query and session-token data. <br>
Mitigation: Review endpoint choices before relying on strictly Zhihu-scoped behavior, and confirm fallback behavior is acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/zhihu-aggregate-scraper) <br>
- [MaxHub API website](https://www.aconfig.cn) <br>
- [Content API reference](artifact/references/api-content.md) <br>
- [Search and trending API reference](artifact/references/api-search-trending.md) <br>
- [User API reference](artifact/references/api-user.md) <br>
- [Parameter mappings](artifact/references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API result summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English responses; requires MAXHUB_API_KEY and curl for live API access.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
