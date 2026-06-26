## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection (Hot Scanner), and rumor/early signal detection. Use for stock analysis, portfolio tracking, earnings reactions, crypto monitoring, trending stocks, or finding rumors before they hit mainstream. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunerw-dev](https://clawhub.ai/user/sunerw-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate stock and crypto analysis, portfolio summaries, watchlist alerts, dividend metrics, trend scans, and rumor/early-signal reports for informational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X scanning may require sensitive session cookies and broad local access. <br>
Mitigation: Use --no-social unless social scanning is required; only configure AUTH_TOKEN and CT0 for trusted use, avoid granting Terminal Full Disk Access unless necessary, and protect any .env file from source control and backups. <br>
Risk: Portfolio and watchlist data can expose personal financial positions or investment interests. <br>
Mitigation: Treat local portfolio and watchlist files as sensitive financial data and limit file access and sharing accordingly. <br>
Risk: Market data, social signals, rumor scans, and generated recommendations may be delayed, incomplete, or misleading. <br>
Mitigation: Use outputs for informational review only and consult qualified financial advice before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunerw-dev/stock-analysis-6) <br>
- [Publisher profile](https://clawhub.ai/user/sunerw-dev) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [README](artifact/README.md) <br>
- [Usage Guide](artifact/docs/USAGE.md) <br>
- [Hot Scanner Guide](artifact/docs/HOT_SCANNER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional JSON output from supporting scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes financial-analysis summaries, recommendations, confidence values, risk flags, portfolio/watchlist records, and trend or rumor scan reports; the artifact states this is not financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved ClawHub release metadata; artifact frontmatter version: 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
