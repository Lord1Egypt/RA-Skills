## Description: <br>
Monitors Chinese tender opportunities through the 标标达/知了标讯 API and helps agents search bid notices, analyze companies and competitors, estimate pricing, and surface expiring projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, sales, and bid strategy teams use this skill to find relevant tender opportunities, inspect tender details, analyze suppliers and competitors, and review market pricing signals from 标标达/知了标讯 data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Procurement research terms, company names, and contact-related queries are sent to an external tender-data provider. <br>
Mitigation: Use the skill only when the 标标达/知了标讯 service is approved for the data being queried, and avoid submitting non-public bid strategy or private customer lists. <br>
Risk: A shared or broadly scoped API key could expose tender research usage or quota to unintended users. <br>
Mitigation: Configure a dedicated ZLBX_API_KEY for agent use and rotate or revoke it according to the organization's credential policy. <br>
Risk: Ambiguous company shorthand can broaden analysis to unintended legal entities. <br>
Mitigation: Ask the agent to show matched companies before broad analyses of shorthand or ambiguous company names. <br>


## Reference(s): <br>
- [招投标商机监控雷达-标标达 on ClawHub](https://clawhub.ai/liu-jiapeng/tender-opportunity-biaobiaoda) <br>
- [标讯搜索类工具 API 详情](references/api-search.md) <br>
- [企业分析类工具 API 详情](references/api-company.md) <br>
- [市场分析类工具 API 详情](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or concise text summaries with structured tender, company, competitor, and pricing analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and sends procurement, company, and contact-related queries to an external 标标达/知了标讯 service.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
