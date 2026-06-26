## Description: <br>
Manages stock and crypto watchlists with AISA live price checks, price targets, stop-loss alerts, and signal-change checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to add, remove, list, and check stock or crypto tickers from a command-line watchlist, with optional target price, stop-loss, and signal-change alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols are sent to the AISA service for live price and signal checks. <br>
Mitigation: Install only if the user trusts the AISA endpoint and is comfortable sharing watchlist tickers with that service. <br>
Risk: Generated prices and BUY/HOLD/SELL signals may be incomplete or misleading for investment decisions. <br>
Mitigation: Treat generated market data and signals as informational, not financial advice. <br>
Risk: The default local state path can be confused with other repository state. <br>
Mitigation: Set CLAWDBOT_STATE_DIR to a dedicated directory when isolating watchlist data matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/stock-watchlist-zh) <br>
- [AISA API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and JSON-backed local watchlist state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; stores watchlist state locally unless CLAWDBOT_STATE_DIR is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
