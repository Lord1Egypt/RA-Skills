## Description: <br>
Research ecommerce categories on Reddit to find opportunity areas, pain points, and trending products using semantic AI search via the reddit-insights.com MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GitYu2016](https://clawhub.ai/user/GitYu2016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce researchers use this skill to search Reddit discussions, identify buyer complaints and product gaps, discover trending products, and produce evidence-backed market research tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on reddit-insights.com and the reddit-insights-mcp npm package, creating ordinary third-party API and package supply-chain risk. <br>
Mitigation: Verify the npm package before running npx and install only if use of reddit-insights.com is acceptable. <br>
Risk: Search queries may disclose confidential product plans, customer data, or sensitive personal information to a third-party service. <br>
Mitigation: Use a dedicated, revocable API key and avoid sending confidential or sensitive data in queries. <br>


## Reference(s): <br>
- [Reddit Insights](https://reddit-insights.com) <br>
- [ClawHub skill page](https://clawhub.ai/GitYu2016/reddit-market-insights) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Chinese research tables, quoted evidence, links, and inline JSON or shell snippets for setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses reddit-insights.com MCP tools and requires REDDIT_INSIGHTS_API_KEY for live searches.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
