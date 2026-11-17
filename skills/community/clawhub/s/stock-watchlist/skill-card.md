## Description:

Query real-time stock prices, basic quote fields, and manage a Markdown watchlist for A-share, Hong Kong, and US stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xhyperdan](https://clawhub.ai/user/0xhyperdan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search A-share, Hong Kong, and US stocks by Chinese name or ticker, inspect current quote fields, and maintain a local Markdown watchlist with position summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Watchlist commands can rewrite or remove rows in a Markdown file.

Mitigation: Keep watchlist files in the project directory and review commands that add, sync, remove, or force-initialize watchlist rows before execution.

Risk: Broad allowed roots could permit watchlist operations outside the intended workspace.

Mitigation: Only set STOCK_WATCHLIST_ALLOWED_ROOTS to explicit directories that are safe for watchlist storage.

Risk: Stock quote data is retrieved from public market APIs and may be delayed, unavailable, or unsuitable as financial advice.

Mitigation: Treat returned quote fields as informational data and verify important trading or investment decisions with authoritative market sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xhyperdan/skills/stock-watchlist)
- [Main stock watchlist script](scripts/stock_watchlist.py)
- [Watchlist Markdown template](assets/watchlist-template.md)
- [Eastmoney search API endpoint](https://searchapi.eastmoney.com/api/suggest/get)
- [Eastmoney quote API endpoint](https://push2.eastmoney.com/api/qt/stock/get)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command output summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update marked sections of a local Markdown watchlist file when watchlist commands are used.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
