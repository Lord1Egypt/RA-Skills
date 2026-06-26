## Description: <br>
Quant Trading Assistant analyzes China A-share market data, calculates technical indicators, screens stocks with simple quantitative rules, and produces informational trading signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query A-share quotes, calculate MA/KDJ/MACD/Bollinger indicators, screen stocks, assess market sentiment, and generate concise analysis reports. Outputs are informational and should be independently verified before trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried stock symbols are sent to Tencent and Sina finance APIs. <br>
Mitigation: Use the skill only when sharing queried symbols with those public market-data services is acceptable. <br>
Risk: Generated trading signals may be incomplete, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Independently verify market data and signals before trading, and treat outputs as informational rather than regulated financial advice. <br>
Risk: The built-in screener is small and simplified. <br>
Mitigation: Review the screening rules and supplement them with broader market, fundamental, and risk analysis before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxie48892-jpg/quant-trading-assistant) <br>
- [Tencent Finance quote API endpoint](https://qt.gtimg.cn/q={symbol}) <br>
- [Sina Finance K-line API endpoint](https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={sina_sym}&scale={scale}&ma=no&datalen={datalen}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports, Python dictionaries, and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on live Tencent and Sina market data availability and may include buy, sell, hold, or watch guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
