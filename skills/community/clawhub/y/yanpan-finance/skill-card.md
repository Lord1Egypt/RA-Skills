## Description: <br>
A-Share Multi-Dimensional Quantitative Analysis MCP Server - broker research reports, AI news analysis, and stock comprehensive analysis <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Li-Evan](https://clawhub.ai/user/Li-Evan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this hosted MCP server to retrieve A-share broker research reports, AI-analyzed company news, and comprehensive stock analysis reports for China-market research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says users are asked to send a bearer token over plain HTTP. <br>
Mitigation: Use only a verified HTTPS endpoint with clear data-handling terms before sending confidential prompts, portfolio details, or API tokens. <br>
Risk: The security evidence reports hardcoded backend database credentials. <br>
Mitigation: Treat the exposed credentials as a publisher security issue that should be removed and rotated before relying on the hosted service. <br>
Risk: The skill returns financial analysis, sentiment, recommendations, and trading decisions. <br>
Mitigation: Review outputs as decision-support information and validate them against independent financial sources before taking investment action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Li-Evan/yanpan-finance) <br>
- [Publisher profile](https://clawhub.ai/user/Li-Evan) <br>
- [Hosted MCP endpoint](http://42.121.167.42:9800/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown-formatted text returned by MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns research report excerpts, news summaries with sentiment and investment recommendations, and stock analysis sections based on company name, date range, limit, or stock code inputs.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
