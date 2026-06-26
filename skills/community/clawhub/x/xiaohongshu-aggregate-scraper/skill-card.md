## Description: <br>
小红书全场景数据查询助手，支持 App 和 Web 多版本 API，覆盖笔记详情、用户数据、搜索、商品、评论和话题等查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, brand teams, analysts, and developers use this skill to query Xiaohongshu notes, users, searches, products, comments, and topics through MaxHub APIs. It supports content research, KOL screening, brand monitoring, and consumer trend analysis with concise Markdown summaries and tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MaxHub API key and may use Xiaohongshu cookies or tokens for some endpoints. <br>
Mitigation: Use scoped or dedicated test credentials where possible, avoid personal browser cookies, keep secrets out of prompts and logs, and rotate or revoke credentials after use. <br>
Risk: Requests and supplied credentials are sent to the third-party MaxHub service at aconfig.cn. <br>
Mitigation: Install only if the user or organization trusts MaxHub/aconfig.cn for the intended data, credentials, and account context. <br>
Risk: Security evidence flags under-scoped scraping/session helpers and an unexpected Douyin fallback path. <br>
Mitigation: Review the skill before deployment and remove or disable fallback or session-helper behavior if a strictly Xiaohongshu-only, read-only assistant is required. <br>
Risk: The skill produces third-party data analysis that may be incomplete, delayed, or unsuitable as the sole source for high-impact decisions. <br>
Mitigation: Treat returned data as reference material and verify important business, compliance, or partnership decisions against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/new-ironman/xiaohongshu-aggregate-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/new-ironman) <br>
- [MaxHub API service](https://www.aconfig.cn) <br>
- [Note API reference](artifact/references/api-note.md) <br>
- [User API reference](artifact/references/api-user.md) <br>
- [Search API reference](artifact/references/api-search.md) <br>
- [Product and topic API reference](artifact/references/api-product-topic.md) <br>
- [Parameter mappings](artifact/references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with concise text, tables, links, and optional curl or environment-variable setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; some endpoints may require Xiaohongshu cookies or tokens supplied by the user.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release evidence, target metadata, and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
