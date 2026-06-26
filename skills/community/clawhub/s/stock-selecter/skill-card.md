## Description: <br>
Stock Selecter screens A-share stocks with 14 configurable fundamental, technical, and market microstructure strategies, supporting single-strategy runs, combined strategy modes, concurrent execution, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alan1121-j](https://clawhub.ai/user/alan1121-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market analysts can use this skill to run configurable A-share stock screens across valuation, profitability, trend, volume, shareholder, cash-flow, and analyst-target signals. It is intended to produce candidate lists and reports for review, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that the skill sends the Tushare token over plain HTTP. <br>
Mitigation: Avoid using the package with sensitive tokens until the API transport is HTTPS or otherwise secured. <br>
Risk: Security evidence reports local result-file creation by default. <br>
Mitigation: Set save=false or provide an explicit output_dir before running in environments where file creation should be controlled. <br>
Risk: Security evidence reports that the shareholder_buyback strategy may rank company repurchase records as shareholder or manager buying signals. <br>
Mitigation: Review shareholder_buyback outputs manually before relying on those results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alan1121-j/stock-selecter) <br>
- [Tushare Pro registration](https://tushare.pro/register) <br>
- [Tushare Pro API documentation](https://tushare.pro/document/2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime output may include JSON, CSV, and HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Tushare token; saves result files by default unless configured otherwise.] <br>

## Skill Version(s): <br>
3.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
