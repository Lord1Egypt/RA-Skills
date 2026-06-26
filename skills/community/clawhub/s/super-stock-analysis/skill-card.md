## Description: <br>
Super Stock Analysis helps agents analyze stocks and cryptocurrencies with Yahoo Finance data, portfolio and watchlist tracking, dividend analysis, multi-factor scoring, trend scanning, and early signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce structured market analysis, portfolio summaries, watchlist alerts, dividend views, and trend or rumor scans for equities and digital assets. Its outputs are informational and should be reviewed before any financial decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external finance, news, and optional social-media data providers. <br>
Mitigation: Run it only in environments where outbound market-data requests are acceptable, and treat returned data as informational rather than authoritative investment advice. <br>
Risk: Portfolio and watchlist workflows store financial tracking data locally. <br>
Mitigation: Use a dedicated workspace or account, review local data paths before use, and avoid entering sensitive account or brokerage credentials. <br>
Risk: Optional Twitter/X setup can use live session credentials such as auth_token and ct0. <br>
Mitigation: Skip the Twitter/X integration unless needed; if used, restrict file access, keep credentials out of shared workspaces, and remove them after scanning. <br>
Risk: The bundled batch_refactor.py script rewrites Python files and is unrelated to normal market analysis. <br>
Mitigation: Do not run batch_refactor.py during normal use; inspect and isolate it before any maintenance use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/subaru0573/super-stock-analysis) <br>
- [MarketPulse Homepage](https://marketpulse.io) <br>
- [README](README.md) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Technical Architecture](docs/ARCHITECTURE.md) <br>
- [Hot Scanner Guide](docs/HOT_SCANNER.md) <br>
- [bird CLI for optional Twitter/X search](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or terminal text with optional JSON from analysis and scanner scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local portfolio, watchlist, cache, and scan-output files under user-local or skill-local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
