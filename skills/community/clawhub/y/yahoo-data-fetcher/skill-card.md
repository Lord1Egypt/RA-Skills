## Description: <br>
Fetch real-time stock quotes from Yahoo Finance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noypearl](https://clawhub.ai/user/noypearl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch current market quote data for one or more stock symbols and return normalized quote fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols queried through the skill are sent to Yahoo Finance. <br>
Mitigation: Use only symbols that are acceptable to share with Yahoo Finance and follow local data handling requirements. <br>
Risk: The skill requires Node.js and network access to the Yahoo Finance quote endpoint. <br>
Mitigation: Confirm Node.js and outbound network access are available before deployment. <br>


## Reference(s): <br>
- [Yahoo Finance quote endpoint](https://query1.finance.yahoo.com/v7/finance/quote) <br>
- [ClawHub skill page](https://clawhub.ai/noypearl/yahoo-data-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns quote objects with symbol, price, change, changePercent, currency, and marketState fields; missing symbols are returned with null quote values.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
