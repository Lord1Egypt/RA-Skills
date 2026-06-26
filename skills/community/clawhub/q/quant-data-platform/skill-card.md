## Description: <br>
Comprehensive quantitative data platform for A-share market. Real-time quotes, historical data, alternative data (sentiment, news, fundamentals), factor data, and data quality monitoring. Essential infrastructure for quantitative trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative analysts use this skill to work with Chinese A-share market data APIs, including quotes, historical bars, alternative data, factor data, and data quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill may present randomly generated market data as real trading data. <br>
Mitigation: Do not use returned data for trading, backtesting, valuation, alerts, or risk decisions unless the implementation fails closed, requires explicit simulation mode, and labels every payload with its true source. <br>
Risk: Testing with market data providers may expose credentials or broaden access. <br>
Mitigation: Use a dedicated low-privilege Tushare token in an isolated environment when evaluating the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/quant-data-platform) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Python usage examples, installation commands, API method descriptions, and configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
