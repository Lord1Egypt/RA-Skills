## Description: <br>
A股、港股、期货量化数据查询工具，基于 Tushare Pro API 通过 HTTP REST 接口获取股票、指数、资金流向、期货和财务数据，无需 pip 或 Python 环境。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloryjack](https://clawhub.ai/user/gloryjack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and quantitative finance users can use this skill to ask an agent for Tushare Pro HTTP request patterns, token setup guidance, and example queries for China A-share, Hong Kong stock, futures, index, money-flow, and financial datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled token.env template points users to a misspelled Tushare-like site while discussing API token setup. <br>
Mitigation: Use the official Tushare site listed in SKILL.md, correct or delete the bundled token.env template, and obtain tokens only through the official account portal. <br>
Risk: Real Tushare API tokens could be exposed if users store them in shared skill files or commit token.env. <br>
Mitigation: Store real tokens securely outside shared artifacts, use a revocable token when possible, and monitor API quota usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gloryjack/tushare-pro) <br>
- [Tushare Pro](https://tushare.pro) <br>
- [Tushare Pro API endpoint](https://api.tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, token configuration snippets, and HTTP API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TUSHARE_TOKEN; available data and rate limits depend on the user's Tushare account permissions and quota.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
