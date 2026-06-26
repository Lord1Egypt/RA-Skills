## Description: <br>
Yahoo Finance (yfinance) powered stock analysis skill: quotes, fundamentals, ASCII trends, high-resolution charts (RSI/MACD/BB/VWAP/ATR), plus optional web add-ons (news + browser-first options/flow). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kys42](https://clawhub.ai/user/kys42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to fetch market quotes and fundamentals, inspect terminal-friendly trends, create chart files with common technical indicators, and gather optional news or options-flow links for market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker, market, and news queries may be sent to external market-data or search providers. <br>
Mitigation: Use the skill only for market research where external lookups are acceptable, and avoid private or sensitive tickers and prompts. <br>
Risk: The optional options-flow helper uses browser automation and third-party page scraping. <br>
Mitigation: Skip the Playwright options-flow helper when browser automation or third-party scraping is not appropriate. <br>
Risk: Python dependencies are installed at execution time and are not fully pinned by the artifact. <br>
Mitigation: Install and run the skill in a virtual environment and review dependencies before deployment. <br>


## Reference(s): <br>
- [Stock Market Pro on ClawHub](https://clawhub.ai/kys42/stock-market-pro) <br>
- [uv package manager](https://github.com/astral-sh/uv) <br>
- [Unusual Whales stock overview](https://unusualwhales.com/stock/{TICKER}/overview) <br>
- [Unusual Whales live options flow](https://unusualwhales.com/live-options-flow?ticker_symbol={TICKER}) <br>
- [Unusual Whales options flow history](https://unusualwhales.com/stock/{TICKER}/options-flow-history) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown, with optional PNG chart files and CHART_PATH output lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market-data and news lookups may contact Yahoo Finance, DuckDuckGo, and optionally Unusual Whales.] <br>

## Skill Version(s): <br>
1.2.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
