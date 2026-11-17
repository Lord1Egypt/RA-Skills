## Description:

Runs Wyckoff-style A-share analysis from stock codes, portfolio holdings, cash, CSV data, and optional chart images using online market data source fallback and Beijing-time trading-session checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngcan-wang](https://clawhub.ai/user/youngcan-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Chinese A-share symbols or portfolios with Wyckoff market-structure reasoning, source-audited market data, and Beijing-time trading-session boundaries. It supports single-stock analysis, holding add/reduce/exit suggestions, candidate rotation comparison, empty-position cash deployment suggestions, and optional chart generation when session rules allow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce concrete add, reduce, exit, switch, or cash-deployment portfolio actions.

Mitigation: Treat those outputs as market analysis for independent review against personal risk tolerance and qualified financial advice, not as instructions to trade.

Risk: The skill depends on online public market data sources that may fail, differ in schema, or return insufficient rows.

Mitigation: Review the data audit table, source used, rows kept, window end date, and fallback count before relying on the analysis.

Risk: Immediate intraday action can be inappropriate outside valid A-share trading windows.

Mitigation: Use the required Beijing-time session verdict and T+1 boundaries; outside tradable sessions, treat outputs as post-market review, next-day planning, or order strategy only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youngcan-wang/skills/wyckoff-a-share)
- [alpha-system-prompt.md](artifact/rules/alpha-system-prompt.md)
- [source-fallbacks.md](artifact/rules/source-fallbacks.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, guidance]

**Output Format:** [Markdown analysis with data audit tables, Chinese-language trading-session status, portfolio action labels, and optional Python plotting code or chart results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include direct-sounding portfolio actions; users should treat them as analysis for review, not instructions to trade.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
