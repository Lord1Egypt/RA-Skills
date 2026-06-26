## Description: <br>
Trades Polymarket U.S. temperature markets using NOAA forecasts, confidence modeling, quality filters, and configurable trade sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mohamedj2020](https://clawhub.ai/user/Mohamedj2020) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect or run automated weather-market trading against Simmer and Polymarket markets, with status and dry-run commands available before live trading. <br>

### Deployment Geography for Use: <br>
Global; the trading strategy targets U.S. weather markets. <br>

## Known Risks and Mitigations: <br>
Risk: Live trading can place real-money market orders when the user deliberately runs or enables it. <br>
Mitigation: Review the source, run dry-run first, use a dedicated Simmer key without withdrawal or account-modification permissions, and expose only a small balance. <br>
Risk: Unattended scheduled runs can trade every six hours if autostart is enabled. <br>
Mitigation: Keep autostart disabled unless prepared for unattended trading, monitor the first live runs, and confirm the stop procedure before enabling automation. <br>
Risk: Optional trade logging dependencies may add behavior beyond the default dependency set. <br>
Mitigation: Leave optional logging packages uninstalled unless needed, and inspect their source and network behavior before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mohamedj2020/weather-trader) <br>
- [Publisher profile](https://clawhub.ai/user/Mohamedj2020) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [NOAA weather API](https://api.weather.gov) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with Python command examples and JSON configuration values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform authenticated Simmer API calls and place real-money trades when live trading is deliberately run or enabled.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
