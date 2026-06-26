## Description: <br>
Weather Trader helps agents scan Polymarket weather markets, compare market prices against NOAA and Open-Meteo forecasts, size trades with EV and Kelly logic, manage open positions, and optionally execute trades through Simmer or Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhlorra](https://clawhub.ai/user/yhlorra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to evaluate and act on weather prediction market opportunities, configure market filters and risk limits, monitor open positions, and review trading performance. It can operate in dry-run analysis mode or live trading mode when API and wallet access are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading can execute financial actions through API or wallet access. <br>
Mitigation: Keep the skill in dry-run mode until the venue, credentials, wallet setup, position limits, and maximum trade count have been reviewed. <br>
Risk: Real-money losses can exceed user expectations if safeguards are weakened or cleared. <br>
Mitigation: Use small maximum position sizes, keep max-trades limits low, avoid --no-safeguards for real-money use, and use --resume only when intentionally clearing the loss circuit breaker. <br>
Risk: Quiet or automated operation can hide important trading decisions and warnings. <br>
Mitigation: Avoid --quiet for real-money runs unless external monitoring and alerting are already in place. <br>
Risk: Local trade logs can expose strategy or account activity. <br>
Mitigation: Review where logs are written and disable, rotate, or protect them when trade history is sensitive. <br>
Risk: Auto-tuning against untrusted skill paths can be unsafe. <br>
Mitigation: Use auto-tuning only with trusted target code and review proposed parameter changes before applying them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yhlorra/yh-polymarket-weather-trader) <br>
- [Simmer Dashboard](https://simmer.markets/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, files] <br>
**Output Format:** [Terminal text and Markdown-style guidance with JSON configuration updates and JSONL trade logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute live trading API calls when live mode, venue, wallet, and credentials are configured; dry run is the default mode.] <br>

## Skill Version(s): <br>
1.16.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
