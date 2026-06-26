## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists, alerts, dividend analysis, 8-dimension stock scoring, viral trend detection, and rumor or early-signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squally2k](https://clawhub.ai/user/squally2k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to analyze equities and supported cryptocurrencies, compare tickers, manage portfolios and watchlists, review dividend metrics, and scan for trending or rumor-driven market signals. Outputs are informational and not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X scanning uses sensitive AUTH_TOKEN and CT0 session cookies and an external CLI with broader access than users may expect. <br>
Mitigation: Prefer non-social scans such as --no-social; if Twitter/X is enabled, keep tokens out of source control, avoid broad terminal permissions, and rotate or revoke exposed sessions. <br>
Risk: Market data, news, short interest, and insider activity can lag or be incomplete, so outputs may be stale or misleading. <br>
Mitigation: Treat analysis as informational, verify material findings against current market sources, and consult a licensed financial advisor before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/squally2k/stock-analysis-6-2-0) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Hot Scanner Documentation](docs/HOT_SCANNER.md) <br>
- [Architecture Documentation](docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Console text or Markdown summaries, with optional JSON output from supported scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local portfolio and watchlist JSON files under the user's ClawDBot skill data directory.] <br>

## Skill Version(s): <br>
6.2.0 (source: SKILL.md frontmatter; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
