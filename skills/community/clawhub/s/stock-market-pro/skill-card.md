## Description:

Yahoo Finance (yfinance) powered stock analysis skill: quotes, fundamentals, ASCII trends, high-resolution charts (RSI/MACD/BB/VWAP/ATR), plus optional web add-ons for news and browser-first options or flow review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kys42](https://clawhub.ai/user/kys42)

### License/Terms of Use:


## Use Case:

External users, developers, and market researchers use this skill to retrieve ticker quotes, summarize fundamentals, inspect terminal trends, create technical-analysis PNG charts, and collect optional market news or options-flow links for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads Python dependencies at runtime and contacts external market-data, search, and options-flow services.

Mitigation: Run it in an isolated environment, review commands before execution, and keep TLS verification enabled for network requests.

Risk: The optional options-flow path may launch headless Chromium with the browser sandbox disabled.

Mitigation: Prefer the browser-first options link helper and use the option scraper only when the added data is necessary.

Risk: Generated chart files in /tmp can be overwritten by later runs using the same ticker.

Mitigation: Move or rename chart outputs after generation when they need to be retained.

## Reference(s):

- [Stock Market Pro on ClawHub](https://clawhub.ai/kys42/skills/stock-market-pro)
- [uv](https://github.com/astral-sh/uv)
- [Unusual Whales stock overview](https://unusualwhales.com/stock/{TICKER}/overview)
- [Unusual Whales live options flow](https://unusualwhales.com/live-options-flow?ticker_symbol={TICKER})
- [Unusual Whales options flow history](https://unusualwhales.com/stock/{TICKER}/options-flow-history)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, files, guidance]

**Output Format:** [Terminal text, Markdown link lists, shell command examples, and PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chart commands write PNG files under /tmp and report commands print CHART_PATH entries.]

## Skill Version(s):

1.2.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
