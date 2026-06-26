## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists, alerts, dividend analysis, stock scoring, trend detection, and early-signal scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run stock, crypto, dividend, portfolio, watchlist, trend, and rumor analyses from command-line workflows. Outputs are informational market analysis and should not be treated as personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional social scanners can expose Twitter/X session cookies or require broad local permissions. <br>
Mitigation: Prefer non-social modes such as --no-social; do not grant Full Disk Access or place Twitter/X session tokens in local configuration unless the account and local-data risk is accepted. <br>
Risk: BUY, HOLD, SELL, trend, and rumor outputs can be mistaken for personalized investment advice. <br>
Mitigation: Treat outputs as informational analysis only and review results with independent sources or a licensed financial advisor before making investment decisions. <br>
Risk: Market, news, and social-source data can be delayed, incomplete, rate-limited, or rumor-driven. <br>
Mitigation: Check source timestamps, rerun analyses when data freshness matters, and verify material findings against authoritative financial and news sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/test-x-sear) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Usage guide](docs/USAGE.md) <br>
- [Hot Scanner documentation](docs/HOT_SCANNER.md) <br>
- [Architecture documentation](docs/ARCHITECTURE.md) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [CoinGecko](https://coingecko.com) <br>
- [Google News](https://news.google.com) <br>
- [bird CLI](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown guidance, shell commands, and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands read market, news, crypto, social, and local portfolio or watchlist data; optional social scanning may require Twitter/X authentication material.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
