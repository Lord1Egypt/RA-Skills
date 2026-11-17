## Description:

Free stock and crypto momentum scanner with social sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nomadrex](https://clawhub.ai/user/nomadrex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to scan stocks and crypto assets for momentum signals, social sentiment, market pulse, score changes, and historical win-rate summaries. Its outputs are informational market-screening aids and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts third-party market and sentiment services and may disclose ticker interests through those requests.

Mitigation: Run it only in environments where those lookups are acceptable, avoid sensitive watchlists, and review the third-party service terms before use.

Risk: Reddit sentiment can use a Tavily API key when TAVILY_API_KEY is present.

Mitigation: Use a scoped key in a dedicated environment, rotate or revoke it as needed, and omit sentiment features when external search is not desired.

Risk: The scanner writes a shared temporary cache that can expose recent scan results on shared systems.

Mitigation: Prefer a dedicated runtime, avoid sudo, clear the cache after use, or run with cache-disabled options where appropriate.

Risk: Momentum and sentiment scores can be incomplete, stale, or misleading for investment decisions.

Mitigation: Treat outputs as informational screening signals and verify results against independent financial data and qualified advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nomadrex/skills/ripe-scanner)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [S&P 500 Companies List](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
- [Nasdaq-100 List](https://en.wikipedia.org/wiki/Nasdaq-100)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text tables and concise Markdown summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked ticker tables, ticker-level profiles, sentiment summaries, market pulse summaries, score-change summaries, and historical win-rate summaries.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
