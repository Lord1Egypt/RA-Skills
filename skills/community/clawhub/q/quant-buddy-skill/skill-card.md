## Description: <br>
Quant Buddy Skill helps agents query A-share, Hong Kong, and U.S. market data and A-share financial metrics, then run screening, factor calculations, backtests, industry aggregation, custom CSV uploads, and chart rendering through QuantBuddy APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pseudo-longinus](https://clawhub.ai/user/pseudo-longinus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and investment research agents use this skill to answer market-data and quant-research requests for A-share, Hong Kong, and U.S. equities, including snapshots, recent-window statistics, financial metrics, screening, backtesting, factor analysis, and charts. It requires a user-provided QuantBuddy API key and can optionally use a Bocha API key for event-study news search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive QuantBuddy credentials and an optional Bocha credential. <br>
Mitigation: Configure credentials locally, avoid pasting API keys into chat, and treat config.json, config.local.json, logs, and output files as sensitive. <br>
Risk: The skill can send user queries, uploaded CSV data, and generated analysis requests to QuantBuddy. <br>
Mitigation: Upload only data that is intended for QuantBuddy processing and avoid confidential or licensed datasets unless the user has authorization. <br>
Risk: The security review advises caution around the zip update flow and local generated artifacts. <br>
Mitigation: Review archives before using update flows and inspect generated output, logs, and cached files before sharing or redeploying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pseudo-longinus/quant-buddy-skill) <br>
- [QuantBuddy skill API endpoint](https://www.quantbuddy.cn/skill) <br>
- [QuantBuddy user API endpoint](https://www.quantbuddy.cn/user) <br>
- [QuantBuddy login and API key page](https://www.quantbuddy.cn/login) <br>
- [Bocha API key page](https://open.bochaai.com) <br>
- [Environment requirements](references/environment.md) <br>
- [Bundled scripts audit](references/scripts-audit.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with tables, JSON/tool parameters, shell commands, and generated chart or CSV file references when workflows request them] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on authenticated QuantBuddy API responses and optional locally generated PNG, CSV, JSON, or HTML artifacts under the skill output directory.] <br>

## Skill Version(s): <br>
4.14.18 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
