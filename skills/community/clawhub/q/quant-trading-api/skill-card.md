## Description: <br>
Professional quantitative trading API integration for Chinese securities that supports major Chinese brokers with order management, position tracking, real-time market data, and automated trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading workflow builders use this skill to prototype Python interfaces for Chinese broker market data, account views, order handling, and strategy automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents live broker trading workflows while the included implementation is mostly simulated. <br>
Mitigation: Treat it as a mock trading prototype until live or paper mode separation, broker behavior, and order-risk controls are clearly verified. <br>
Risk: The examples involve brokerage account credentials. <br>
Mitigation: Do not enter real brokerage credentials; test only in an isolated Python environment and use reviewed secret handling before any real integration. <br>
Risk: Quotes, balances, positions, and order results may be mock or inaccurate. <br>
Mitigation: Do not rely on the outputs for financial decisions or real orders without independent validation and explicit risk limits. <br>


## Reference(s): <br>
- [Quant Trading Api on ClawHub](https://clawhub.ai/jason-aka-chen/quant-trading-api) <br>
- [jason-aka-chen publisher profile](https://clawhub.ai/user/jason-aka-chen) <br>
- [Huatai API documentation](https://openapi.htsc.com) <br>
- [Galaxy API documentation](https://api.galaxy.com) <br>
- [Tushare API](https://tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Python API examples and configuration snippets; treat trading data and order behavior as prototype output unless verified against a live or paper brokerage environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
