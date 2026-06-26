## Description: <br>
Stock Tools helps an agent maintain a local A-share watchlist and fetch lightweight public quotes for individual stocks or the saved watchlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daguniang](https://clawhub.ai/user/daguniang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to manage a persistent A-share watchlist and answer current quote or watchlist-performance questions in natural language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock codes and quote requests are sent to a public quote service. <br>
Mitigation: Use the skill only when public quote lookup is acceptable for the requested stocks. <br>
Risk: The watchlist is stored in a local file, and a custom --file path can point the script at another file. <br>
Mitigation: Use the default stocks-data/stocklist.txt location unless intentionally selecting a separate watchlist file. <br>
Risk: Quotes may be unavailable, stale, or invalid outside normal market conditions. <br>
Mitigation: Treat unavailable or unconfirmed quote timestamps as uncertainty and avoid fabricating market data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daguniang/stock-tools) <br>
- [Sina public quote endpoint](https://hq.sinajs.cn/list=...) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>
- [Tonghuashun stock detail page pattern](https://stockpage.10jqka.com.cn/{code}/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Concise natural-language stock summaries, line-oriented text, and optional JSON quote records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write a local stocks-data/stocklist.txt watchlist; quote availability depends on the public market data source and trading-state timing.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
