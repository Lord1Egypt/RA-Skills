## Description: <br>
Trades Polymarket markets where PolyClawster whale signals are active by fetching smart-money scores and buying YES or NO positions through the Simmer SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhlorra](https://clawhub.ai/user/yhlorra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders and agent operators use this skill to scan Polymarket for high-conviction whale signals, review matching markets, and optionally place position-sized trades. It supports dry-run scanning, live trading, minimum-score filtering, and position status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can open multiple real-money Polymarket positions in one run without a final confirmation or aggregate run limit. <br>
Mitigation: Start with dry run or TRADING_VENUE=sim, use --live only after reviewing matched markets, and verify that the Simmer account has the intended permissions. <br>
Risk: Position sizing is driven by external smart-money scores and the configured maximum position size. <br>
Mitigation: Set SIMMER_SMARTMONEY_MAX_POSITION conservatively and pass --min-score explicitly for each run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yhlorra/yh-polymarket-smart-money) <br>
- [Publisher Profile](https://clawhub.ai/user/yhlorra) <br>
- [PolyClawster Signals API](https://polyclawster.com/api/signals) <br>
- [Simmer Dashboard](https://simmer.markets/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Console text with command-line options and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; live trading depends on --live and the configured trading venue.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
