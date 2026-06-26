## Description: <br>
Check stock prices using yfinance library. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request current stock and ETF price snapshots through the documented local command workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock price output could be combined with personal identifiers or portfolio details. <br>
Mitigation: Return only the requested market data and avoid correlating ticker output with names, account numbers, holdings, or personal financial amounts. <br>
Risk: Financial data could be sent to external services or listeners. <br>
Mitigation: Use the documented local stock-price command and do not pipe results into network-transmitting commands or construct outbound requests from the data. <br>
Risk: Bypassing the documented command path can remove the skill's error handling and safety boundaries. <br>
Mitigation: Run only the documented single-symbol command pattern and avoid inline yfinance imports, script modifications, or alternate commands for this skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/stock-price-checker-hardened) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/stock-price-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text stock quote summary, with Markdown command examples in skill guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs symbol, price, daily change, volume, average volume, and average-volume percentage when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
