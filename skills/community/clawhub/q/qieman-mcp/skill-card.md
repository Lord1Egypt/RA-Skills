## Description: <br>
Connects agents to the Qieman MCP service through qieman-mcp-cli for fund lookup, financial news, portfolio analysis, risk analysis, backtesting, chart rendering, and PDF generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joey-lucky](https://clawhub.ai/user/joey-lucky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to retrieve Qieman finance data and perform fund, strategy, portfolio, risk, cash-flow, and market analysis through qieman-mcp-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup workflow can involve login, SMS verification, agreement acceptance, and API-key storage. <br>
Mitigation: Complete login, SMS verification, agreement acceptance, and API-key copying yourself outside the agent whenever possible. <br>
Risk: The skill can process personal, household, portfolio, and other financial data. <br>
Mitigation: Share only the financial data you intend to send to Qieman and avoid exposing raw API keys or SMS codes in chat unless you accept that risk. <br>
Risk: The release security verdict is suspicious because of the amount of control requested during setup. <br>
Mitigation: Install only after reviewing the skill and qieman-mcp-cli, and use it only if you trust the publisher and Qieman service. <br>


## Reference(s): <br>
- [qieman-mcp ClawHub release page](https://clawhub.ai/joey-lucky/qieman-mcp) <br>
- [且慢 MCP 初始化工作流](references/初始化工作流.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI inputs; tool results may include structured text, chart URLs, and PDF URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires qieman-mcp-cli and a configured API key; finance workflows may process user-provided portfolio, household, or financial data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
