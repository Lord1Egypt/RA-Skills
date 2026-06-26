## Description: <br>
Zhipu Search provides web search through the Zhipu AI API with selectable search engines, recency and domain filters, result counts, and content-size controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyhit2005](https://clawhub.ai/user/whyhit2005) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve recent web information through Zhipu AI search, including standard, advanced, Sogou, and Quark-backed searches with optional recency, domain, count, and content-detail controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and optional user_id values are sent to Zhipu AI. <br>
Mitigation: Use a dedicated Zhipu API key, avoid sensitive private queries, and do not pass real names, emails, or account IDs as user_id values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whyhit2005/whyhit2005-zhipu-search) <br>
- [Zhipu AI API endpoint](https://open.bigmodel.cn/api/paas/v4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON search results with titles, summaries, links, source metadata, and optional search-intent details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; sends search queries and optional user_id values to Zhipu AI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
