## Description: <br>
Analyzes stocks and cryptocurrencies with Yahoo Finance data, portfolio and watchlist tracking, dividend metrics, stock scoring, trend detection, and rumor scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run command-line stock, crypto, dividend, portfolio, watchlist, trend, and rumor analyses for informational market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X scanning can expose live AUTH_TOKEN and CT0 session credentials to an external CLI. <br>
Mitigation: Use finance-only commands or run the hot scanner with --no-social unless social-media data is required; do not provide AUTH_TOKEN or CT0 unless the credential exposure is acceptable. <br>
Risk: The Twitter/X setup may require broad local permissions such as Terminal Full Disk Access. <br>
Mitigation: Avoid granting broad local permissions casually, and keep any .env file containing session credentials out of shared folders and repositories. <br>
Risk: Market, short-interest, filing, news, and social signals may be delayed, cached, rate-limited, or keyword-based. <br>
Mitigation: Treat outputs as informational market research, verify important claims against primary sources, and do not use the skill as financial advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/udiedrichsen/stock-analysis) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Stock Analysis README](artifact/README.md) <br>
- [Usage Guide](artifact/docs/USAGE.md) <br>
- [Hot Scanner Documentation](artifact/docs/HOT_SCANNER.md) <br>
- [Architecture Notes](artifact/docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text and optional JSON, with command examples and local configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local portfolio, watchlist, and scanner cache JSON files under user or skill storage paths.] <br>

## Skill Version(s): <br>
6.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
