## Description: <br>
Query real-time stock prices, basic quote fields, and manage a Markdown watchlist for A-share, Hong Kong, and US stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xhyperdan](https://clawhub.ai/user/0xhyperdan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to resolve stock names or ticker symbols, retrieve current quote fields, and maintain a Markdown watchlist with optional cost and position summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock lookup terms are sent to Eastmoney during search and quote requests. <br>
Mitigation: Install and use the skill only if sending those lookup terms to Eastmoney is acceptable. <br>
Risk: Watchlist commands edit local Markdown files. <br>
Mitigation: Keep the watchlist in a dedicated file such as ./watchlist.md, avoid sensitive account data, and configure STOCK_WATCHLIST_ALLOWED_ROOTS only for directories intended for edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xhyperdan/stock-watchlist) <br>
- [Stock watchlist script](scripts/stock_watchlist.py) <br>
- [Watchlist template](assets/watchlist-template.md) <br>
- [Eastmoney search API](https://searchapi.eastmoney.com/api/suggest/get) <br>
- [Eastmoney quote API](https://push2.eastmoney.com/api/qt/stock/get) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summaries, JSON command output, and Markdown watchlist files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Watchlist edits are scoped to Markdown files inside the current working directory unless STOCK_WATCHLIST_ALLOWED_ROOTS is explicitly configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
