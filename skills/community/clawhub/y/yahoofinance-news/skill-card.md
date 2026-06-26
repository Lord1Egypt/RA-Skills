## Description: <br>
Fetch recent finance news headlines for stock, ETF, and index symbols via Yahoo Finance (yfinance), with caching and structured JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phonphrm](https://clawhub.ai/user/phonphrm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch and summarize recent Yahoo Finance headlines for requested stock, ETF, or index symbols, including publisher, publication time, and links. It is intended for informational market-news summaries, not trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested ticker symbols are sent to Yahoo Finance through yfinance. <br>
Mitigation: Use the skill only for explicit ticker or Yahoo Finance news requests and avoid submitting sensitive or unintended symbols. <br>
Risk: Public headline results are cached locally under .cache/finance-news. <br>
Mitigation: Clear the cache when local retention is not desired and use --no-cache or a short --ttl for fresher results. <br>
Risk: Broad trigger wording could cause an agent to choose this skill for general news requests. <br>
Mitigation: Route to this skill only when the user asks for stock, ETF, index, ticker, or Yahoo Finance news. <br>
Risk: Yahoo Finance coverage is unofficial, best-effort, and may be incomplete or stale. <br>
Mitigation: Present results as informational headlines, include item URLs, and avoid trading-advice phrasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phonphrm/yahoofinance-news) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/phonphrm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [JSON from the helper script and concise Markdown summaries with per-item URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and yfinance; supports symbol, limit, ttl, and no-cache options; caches public headline results under .cache/finance-news.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
