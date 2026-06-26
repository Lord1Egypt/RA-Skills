## Description: <br>
Quant is a quantitative investing assistant for market data retrieval, factor calculations, backtesting, risk monitoring, and trading signal guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[77Spongebob](https://clawhub.ai/user/77Spongebob) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, investors, and analysts can use this skill to fetch market data, calculate quantitative factors, run strategy backtests, monitor risk, and produce trading signal guidance. Outputs should be reviewed before being used for financial decisions or account-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Third-party financial data services and local configuration can expose credentials if tokens are stored or shared carelessly. <br>
Mitigation: Keep provider tokens in private local settings or environment variables, avoid committing config files with secrets, and review provider terms before use. <br>
Risk: Dependency installation wording may be incomplete and could hide package installation commands. <br>
Mitigation: Ask to see the exact dependency-install commands before running `quant install`, then approve only commands you understand. <br>
Risk: Backtests, risk metrics, and trading signals can be misleading or unsuitable for live trading. <br>
Mitigation: Treat outputs as informational, validate assumptions against independent data, and require explicit approval before any account-changing action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/77Spongebob/quant) <br>
- [Tushare token registration](https://tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples, Python code, and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local configuration, third-party market data services, and user-approved trading signal workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
