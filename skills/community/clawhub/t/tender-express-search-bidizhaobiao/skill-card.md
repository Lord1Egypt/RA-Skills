## Description: <br>
地方标讯极速检索-比地招标，当用户指定省份、城市或特定地域进行下沉标讯搜索时调用，必须严格应用地域过滤器参数，快速返回按时间倒序排列的地方采购公告及预算金额。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External procurement analysts, sales teams, and agent users use this skill to search Chinese tender notices by keyword, geography, amount, and date, then retrieve details or summarize local opportunities. It also supports company, competitor, contact, and market-intelligence lookups when those broader procurement-analysis workflows are requested. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags that this skill exposes broader company, contact, competitor, and market-intelligence features than the local tender-search description suggests. <br>
Mitigation: Use it only when the full procurement-intelligence scope is acceptable, and require explicit user intent before company expansion, contact lookup, competitor analysis, or market aggregation. <br>
Risk: The skill requires a sensitive API key and can consume account quota. <br>
Mitigation: Use a dedicated ZLBX_API_KEY, store it in the agent environment or approved secret store, monitor quota, and avoid exposing the key in prompts or logs. <br>
Risk: Search terms, company names, and contact lookups may reveal sensitive business interests to an external procurement API. <br>
Mitigation: Avoid confidential search terms, apply region filters when needed, and review results before sharing them outside the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/tender-express-search-bidizhaobiao) <br>
- [Bidizhaobiao API key setup](https://ai.zhiliaobiaoxun.com/?ch=s27) <br>
- [Tender Search API Reference](references/api-search.md) <br>
- [Company Analysis API Reference](references/api-company.md) <br>
- [Market Analysis API Reference](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries with JSON API request examples and retrieved procurement data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and may consume API quota for each request.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
