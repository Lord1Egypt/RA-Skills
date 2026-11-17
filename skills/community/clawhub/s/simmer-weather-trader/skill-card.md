## Description:

Automated weather prediction market trading skill for Simmer/Polymarket that cross-references NOAA, Open-Meteo, Wunderground, and NVIDIA FourcastNet forecasts before placing consensus-based weather market trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrjoeteam](https://clawhub.ai/user/mrjoeteam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt a Telegram-based Simmer weather market trading bot that combines live weather forecasts, NVIDIA FourcastNet output, and Simmer market context before deciding whether to buy YES shares.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose account details and trigger trades through Telegram without authorization checks.

Mitigation: Add Telegram user allowlisting and local confirmation before status lookup or trade execution.

Risk: Documented dry-run and live-trading controls do not match the reviewed code behavior.

Mitigation: Implement and test an explicit dry-run default, a live-trading gate, and trade amount limits before using real credentials.

Risk: The bot depends on browser-based Wunderground scraping and several live services that can fail or change behavior.

Mitigation: Run in isolated infrastructure, pin dependencies, monitor service failures, and require graceful no-trade behavior when any source is unavailable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mrjoeteam/skills/simmer-weather-trader)
- [Simmer API base](https://api.simmer.markets)
- [NVIDIA FourcastNet endpoint](https://climate.api.nvidia.com/v1/nvidia/fourcastnet)
- [NOAA Weather API](https://api.weather.gov)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Wunderground forecast page](https://www.wunderground.com/forecast/us)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance and Python code with shell setup commands and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram messages, logs, API requests, and trade execution calls when deployed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
