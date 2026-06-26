## Description: <br>
热门标讯挖掘助手-火标网，当用户需要进行行业热度分析、统计Top采购商或聚合近期高频中标记录时调用，调用多维度聚合统计接口，呈现特定行业的市场热度与集中度趋势。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business analysts, sales teams, and procurement researchers use this skill to query Huobiaowang/Zhiliaobiaoxun tender data, identify active purchasers and suppliers, analyze company bidding activity, and summarize market concentration or price trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends tender, company, and market-intelligence queries to an external Huobiaowang/Zhiliaobiaoxun API provider. <br>
Mitigation: Use it only when the API provider is trusted and configure ZLBX_API_KEY with the minimum access needed for the intended workflow. <br>
Risk: Company contact and affiliate or subsidiary results may contain sensitive business contact-style data or imprecise entity matches. <br>
Mitigation: Treat returned contact data as sensitive and ask the agent to confirm matched subsidiaries or affiliates before relying on broad company analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/trending-miner-huobiaowang) <br>
- [API key registration](https://ai.zhiliaobiaoxun.com/?ch=s28) <br>
- [标讯搜索类工具 API 详情](references/api-search.md) <br>
- [企业分析类工具 API 详情](references/api-company.md) <br>
- [市场分析类工具 API 详情](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown summaries with structured API request and response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY for API access.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
