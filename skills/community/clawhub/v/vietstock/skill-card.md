## Description: <br>
Automated Vietnamese stock price and index checking on FireAnt.vn for current stock prices, market indices, trading volumes, and financial information for Vietnamese stocks and market indices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aholake](https://clawhub.ai/user/aholake) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to retrieve FireAnt.vn stock and index data for Vietnamese equities and market indices from ticker or index symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens Google and FireAnt.vn through browser automation to retrieve stock data. <br>
Mitigation: Use normal stock symbols or index names as input and avoid arbitrary URLs or unusual strings. <br>
Risk: Market data fetched from live web pages may be unavailable, stale, or parsed incorrectly. <br>
Mitigation: Review the returned data against FireAnt.vn or another trusted market data source before relying on it. <br>


## Reference(s): <br>
- [FireAnt stock and index pages](https://fireant.vn/ma-chung-khoan/{SYMBOL}) <br>
- [ClawHub skill page](https://clawhub.ai/aholake/vietstock) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Formatted text with Markdown emphasis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one text stream containing price or index value, trading volume, market metrics, and error messages when data is unavailable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
