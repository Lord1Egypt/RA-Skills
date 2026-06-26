## Description: <br>
Generate professional technical analysis charts with candlesticks, Fibonacci levels, SMA 20/50, RSI, and pattern detection for crypto and commodities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NomadRex](https://clawhub.ai/user/NomadRex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate technical-analysis chart images and summaries for BTC, ETH, XRP, SUI, Gold, and Silver. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chart images may be sent to a fixed Telegram recipient without the user's selected destination or confirmation. <br>
Mitigation: Remove or replace the hard-coded Telegram target and require explicit destination confirmation before sending chart images externally. <br>
Risk: Chart generation depends on a local crypto_charts.py file whose behavior is outside the skill card evidence. <br>
Mitigation: Use only a trusted local crypto_charts.py file and review it before running chart-generation commands. <br>


## Reference(s): <br>
- [Stock TA Charts ClawHub release page](https://clawhub.ai/NomadRex/stock-ta-charts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Guidance] <br>
**Output Format:** [Markdown instructions with bash code blocks; generated PNG chart files and console summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chart generation relies on a trusted local crypto_charts.py module and external market data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
