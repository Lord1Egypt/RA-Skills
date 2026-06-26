## Description: <br>
查询 A 股上市公司业绩快报数据，支持沪深京股票。当用户询问股票业绩快报、营收、净利润、EPS、ROE、同比增长、一季报、半年报、三季报、年报等财务指标时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lv19944516](https://clawhub.ai/user/lv19944516) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query performance express data for one A-share stock code and present revenue, profit, EPS, ROE, and related period metrics in a readable table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried stock codes are sent to the configured market data service. <br>
Mitigation: Use the skill only when sharing the requested stock code with the configured endpoint is acceptable. <br>
Risk: Changing BASE_URL can send requests to a replacement endpoint with different trust or data-handling properties. <br>
Mitigation: Keep the default endpoint unless the replacement service is trusted and approved for the environment. <br>
Risk: Financial metrics depend on external API availability and data freshness. <br>
Mitigation: Verify important financial decisions against authoritative market or issuer sources before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lv19944516/test-stock-performance-express) <br>
- [Market data API service](https://market.ft.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown table with a heading and record count.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one validated stock code per query; missing API fields are displayed as N/A.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
