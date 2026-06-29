## Description: <br>
Query Taiwan mutual fund NAV, performance, holdings via cnyes/MoneyDJ, compare funds, and perform automatic currency conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichendong](https://clawhub.ai/user/ichendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Taiwan mutual fund NAV, performance, fund comparisons, benchmark performance, and currency conversion from public financial-data services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends fund codes, fund names, symbols, and exchange-rate requests to public financial-data services. <br>
Mitigation: Use only non-sensitive lookup inputs and review the listed data sources before running commands in sensitive environments. <br>
Risk: The TDCC command stores a local NAV cache under ~/.openclaw/cache/taiwan-fund/. <br>
Mitigation: Treat the cache as local financial lookup data and remove it when it is no longer needed. <br>
Risk: Financial outputs may be incomplete, stale, or unsuitable as investment advice. <br>
Mitigation: Treat outputs as informational data and verify decisions against authoritative financial sources. <br>


## Reference(s): <br>
- [ClawHub Taiwan Fund skill page](https://clawhub.ai/ichendong/taiwan-fund) <br>
- [cnyes fund detail pages](https://invest.cnyes.com/funds/detail/{name}/{code}/overview) <br>
- [TDCC OpenAPI offshore fund NAV endpoint](https://openapi-t.tdcc.com.tw/v1/opendata/3-4) <br>
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5y&interval=1d) <br>
- [open.er-api.com exchange-rate endpoint](https://open.er-api.com/v6/latest/USD) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live financial data, fund comparisons, exchange-rate conversions, and cache status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
