## Description: <br>
获取A股股票实时行情数据并进行技术分析。适用于投资者查询股票价格、涨跌幅、成交量等行情信息，以及进行MA、RSI、MACD等技术指标分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[will1189](https://clawhub.ai/user/will1189) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to look up A-share stock quotes from Eastmoney and generate basic MA, RSI, and MACD technical analysis. Outputs should be treated as informational market analysis, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock analysis outputs could be mistaken for personalized financial advice. <br>
Mitigation: Present outputs as informational market analysis and avoid making personalized investment recommendations. <br>
Risk: Stock queries contact Eastmoney over the network and may expose queried stock codes to that site. <br>
Mitigation: Tell users that requested stock codes are sent to Eastmoney and keep query volume modest. <br>
Risk: Eastmoney page structure or network availability may change and cause incomplete or stale data. <br>
Mitigation: Validate fetched fields before analysis and retry or update parsing when data is missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/will1189/stock-acquisition-analysis) <br>
- [Eastmoney Shanghai quote page pattern](https://quote.eastmoney.com/sh{stock-code}.html) <br>
- [Eastmoney Shenzhen quote page pattern](https://quote.eastmoney.com/sz{stock-code}.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with structured quote fields and technical indicators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock prices, percentage changes, volume, market value, MA, RSI, MACD, and simple buy/sell signal interpretation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
