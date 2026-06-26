## Description: <br>
Professional US stock radar for screening, deep dives, and watchlist alerts using public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyfree](https://clawhub.ai/user/spyfree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to screen US equities, run single-ticker deep dives, and monitor watchlists with timestamped heuristic signals, confidence, sources, and data-gap caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried ticker symbols are sent to public finance data providers. <br>
Mitigation: Use only symbols and watchlists that are acceptable to disclose to Yahoo Finance and Stooq public endpoints. <br>
Risk: Free market-data endpoints may be delayed, partial, unavailable, or rate-limited. <br>
Mitigation: Review the output's availability, data_gaps, degraded_mode, confidence, and sources fields before relying on the analysis. <br>
Risk: The output is heuristic market research support and may be mistaken for investment advice. <br>
Mitigation: Present grades and rankings as signal triage only, avoid deterministic predictions, and require independent review before any trading decision. <br>
Risk: The script depends on the local Python environment and the requests package. <br>
Mitigation: Install and run it only in a trusted environment with reviewed dependencies. <br>


## Reference(s): <br>
- [Metrics Reference](references/metrics.md) <br>
- [US Stock Radar on ClawHub](https://clawhub.ai/spyfree/us-stock-radar) <br>
- [Yahoo Finance quote API](https://query1.finance.yahoo.com/v7/finance/quote) <br>
- [Yahoo Finance chart API](https://query1.finance.yahoo.com/v8/finance/chart) <br>
- [Yahoo Finance quoteSummary API](https://query2.finance.yahoo.com/v10/finance/quoteSummary) <br>
- [Stooq daily quote endpoint](https://stooq.com/q/l/) <br>
- [Stooq daily history endpoint](https://stooq.com/q/d/l/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Plain-text narrative plus JSON payloads with timestamp, mode, event_mode, availability, data_gaps, degraded_mode, confidence, sources, and heuristic notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports screener, deep-dive, and watchlist modes; pro or beginner explanations; English or Chinese narrative output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
