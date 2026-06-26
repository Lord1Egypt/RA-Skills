## Description: <br>
获取 TradeAlpha 实时新闻和语义检索结果，适用于 TradeAlpha 新闻、今日新闻、路透、彭博、Truth、国内资讯、研报快讯，以及按主题、事件、公司或叙事检索相关新闻的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tradealpha-coder](https://clawhub.ai/user/tradealpha-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve TradeAlpha realtime news lists and semantic news search results, then summarize key Chinese-language findings. It requires a user-provided TradeAlphaToken in chat and reuses that token only within the current conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires users to paste a TradeAlpha token into chat and sends it to the listed TradeAlpha API domains. <br>
Mitigation: Use a limited-scope or easily revocable token, verify the TradeAlpha site, and rotate the token or start a fresh conversation when session reuse is no longer desired. <br>
Risk: Realtime news may have the documented 0-5 minute objective delay. <br>
Mitigation: Tell users when recency matters and avoid presenting results as perfectly instantaneous. <br>


## Reference(s): <br>
- [TradeAlpha News Reference](references/reference.md) <br>
- [TradeAlpha News Examples](references/examples.md) <br>
- [TradeAlpha official site](https://quantaccess.lxaa.top/) <br>
- [Realtime news endpoint](https://openapi.lxaa.top/api/v1/news/realtime_news) <br>
- [Semantic search endpoint](https://openapi.lxaa.top/api/v1/news/news_vector_search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summaries with structured JSON request and response details when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a chat-provided TradeAlphaToken; does not use environment variables or local token storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 2.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
