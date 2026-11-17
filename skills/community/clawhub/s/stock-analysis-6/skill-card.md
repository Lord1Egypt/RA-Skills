## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists and alerts, dividend analysis, 8-dimension stock scoring, viral trend detection, and rumor or early signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunerw-dev](https://clawhub.ai/user/sunerw-dev)

### License/Terms of Use:


## Use Case:

External users, developers, and investment-focused agents use this skill to analyze US stocks and supported cryptocurrencies, compare tickers, manage local portfolios and watchlists, and scan market, news, and social signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Twitter/X scanner paths handle AUTH_TOKEN and CT0 account-session credentials and pass the local environment to the external bird CLI.

Mitigation: Use --no-social when social scanning is not required, keep credentials scoped to this skill, and review the bird CLI and dependency chain before enabling Twitter/X scanning.

Risk: The skill stores portfolio and watchlist data locally and explicit commands can modify or delete those files.

Mitigation: Back up local portfolio and watchlist files before using update, remove, or delete commands, and review command arguments before execution.

Risk: Market data, scanner signals, and rumor impact scores can be delayed, incomplete, or misleading.

Mitigation: Treat outputs as informational, verify important findings against authoritative financial sources, and consult a licensed financial advisor before investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunerw-dev/skills/stock-analysis-6)
- [Publisher Profile](https://clawhub.ai/user/sunerw-dev)
- [Yahoo Finance](https://finance.yahoo.com)
- [Usage Guide](docs/USAGE.md)
- [Hot Scanner Documentation](docs/HOT_SCANNER.md)
- [Architecture Documentation](docs/ARCHITECTURE.md)
- [Concept Documentation](docs/CONCEPT.md)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Console text and JSON, with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio, watchlist, and scanner cache files under the skill's configured local storage paths.]

## Skill Version(s):

1.0.0 (source: server release metadata); source skill frontmatter reports 6.2.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
