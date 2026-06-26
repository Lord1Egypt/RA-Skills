## Description: <br>
Stock technical analysis scanner based on swing trading principles with multi-timeframe resonance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddieguan801-oss](https://clawhub.ai/user/eddieguan801-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local Python-based stock scans that analyze ticker symbols for multi-timeframe trend alignment, MACD status, volume-price behavior, support and resistance levels, and composite buy, sell, or hold-style signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates buy, sell, and hold-style technical-analysis signals that could be mistaken for professional financial advice. <br>
Mitigation: Treat outputs as educational technical-analysis summaries and verify investment decisions with independent research or a qualified financial professional. <br>
Risk: The Python scanner contacts yfinance/Yahoo and depends on third-party market data and packages. <br>
Mitigation: Run it only in an environment where local Python execution and outbound market-data requests are acceptable. <br>


## Reference(s): <br>
- [Sample Stock Scanner Output](artifact/references/sample_output.md) <br>
- [ClawHub skill page](https://clawhub.ai/eddieguan801-oss/stock-trend-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and terminal text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ticker-level reports and a ranked stock table; results depend on yfinance/Yahoo market data availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
