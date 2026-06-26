## Description: <br>
Find and filter stocks by financial metrics, fundamentals, and technical indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saintlittlefish](https://clawhub.ai/user/saintlittlefish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and financial-analysis users can use this skill to run stock screens by valuation, dividend, market-cap, sector, growth, momentum, and volume criteria, then save or inspect watchlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes billing files with a hardcoded SkillPay API key and unclear charge authorization. <br>
Mitigation: Do not enable or invoke the billing integration until the publisher removes embedded credentials, documents explicit user approval before charges, and aligns billing text with the stock screener. <br>
Risk: Watchlist names are used when writing files. <br>
Mitigation: Use simple watchlist names without slashes or path components. <br>
Risk: Stock-screening output depends on external financial data and a limited predefined ticker universe. <br>
Mitigation: Review results against authoritative financial sources before using them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/saintlittlefish/xanadu-stock-screener) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, tabular terminal output, and JSON watchlist files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screens a fixed stock universe through yfinance and may save watchlists under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
