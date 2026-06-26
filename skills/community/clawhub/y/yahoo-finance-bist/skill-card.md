## Description: <br>
Provides Yahoo Finance based market analysis, technical indicator scoring, historical data export, portfolio alerts, and trade logging for BIST, U.S. equities, crypto, commodities, and currency pairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nikolayco](https://clawhub.ai/user/Nikolayco) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and finance-focused agents use this skill to fetch Yahoo Finance market data, run technical indicators, export historical price data, maintain portfolio alerts, and record buy or sell activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python scripts that can create or change watchlists, alerts, trade logs, CSVs, and HTML reports on disk. <br>
Mitigation: Run explicit commands only after confirming the intended action, symbol, quantity, price, and install path; periodically review or delete generated JSON, CSV, and HTML files. <br>
Risk: Broad finance prompts can trigger record-changing behavior without enough scoping or confirmation. <br>
Mitigation: Require confirmation before buy, sell, add, remove, or report commands, and treat analysis output as informational rather than as a substitute for financial review. <br>
Risk: The scripts contact Yahoo Finance over the network to fetch market data. <br>
Mitigation: Install and run the skill only where outbound Yahoo Finance requests are acceptable and avoid sensitive or untrusted symbol and name inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nikolayco/yahoo-finance-bist) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Nikolayco) <br>
- [Yahoo Finance chart endpoint used by scripts](https://query1.finance.yahoo.com/v8/finance/chart/{symbol}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, CSV, and HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may update portfolio_alerts.json and trade_history.json and may generate Nikos_Islem_Gecmisi.csv and Nikos_Portfoy_Analiz.html.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
