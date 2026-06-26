## Description: <br>
Query real-time stock data using Tencent Finance API for Chinese A-shares, Hong Kong stocks, US stocks, and indices, including market cap, valuation, volume, turnover, total shares, and 52-week range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangzhe1991](https://clawhub.ai/user/yangzhe1991) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current quote data and basic market metrics for supported A-share, Hong Kong, US, and index symbols from Tencent Finance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols queried by the user are sent to Tencent Finance over an unencrypted HTTP request. <br>
Mitigation: Use only when sending requested ticker symbols to Tencent Finance over HTTP is acceptable. <br>
Risk: Market quotes and valuation metrics can be incomplete, stale, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Treat returned quote data as informational and verify important financial decisions with authoritative market data sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangzhe1991/tencent-finance-stock-price) <br>
- [Tencent Finance quote endpoint](http://qt.gtimg.cn) <br>
- [Publisher profile](https://clawhub.ai/user/yangzhe1991) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text table with optional detailed quote sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are derived from live Tencent Finance responses for the ticker symbols supplied by the user.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
