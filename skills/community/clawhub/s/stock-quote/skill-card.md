## Description: <br>
Fetches stock quotes and fundamental data for one or more ticker symbols from Stooq, yfinance, Financial Modeling Prep, or Yahoo Finance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linux2010](https://clawhub.ai/user/linux2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve ticker quote fields for portfolio updates, pre-trade price checks, and valuation workflows. It supports single-symbol and bulk quote requests with text or JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default source can return delayed data despite real-time wording. <br>
Mitigation: Check the returned source, date, and timestamp before using results, and choose an explicit real-time-capable source when freshness matters. <br>
Risk: Ticker symbols are sent to external finance services. <br>
Mitigation: Use the skill only when sharing the requested symbols with those services is acceptable. <br>
Risk: Quote values may be unavailable, stale, or rate-limited. <br>
Mitigation: Check the returned error field and verify data independently before trading, compliance, or valuation decisions. <br>


## Reference(s): <br>
- [Stock Data API Sources](references/api-sources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linux2010/stock-quote) <br>
- [Stooq CSV Quote Endpoint](https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlc&h=&t=csv) <br>
- [Financial Modeling Prep](https://financialmodelingprep.com) <br>
- [Yahoo Finance Quote Pages](https://finance.yahoo.com/quote/{SYMBOL}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API calls] <br>
**Output Format:** [Plain text quote summaries or JSON objects with symbol, price, source, timestamp, and related market fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bulk ticker input is supported; results may include an error field when a provider fails or a symbol is invalid.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
