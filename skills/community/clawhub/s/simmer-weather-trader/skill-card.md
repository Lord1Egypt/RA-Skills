## Description: <br>
Automated weather prediction market trading skill for Simmer/Polymarket that cross-references NOAA, Open-Meteo, Wunderground, and NVIDIA FourcastNet forecasts before recommending or placing trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrjoeteam](https://clawhub.ai/user/mrjoeteam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-bot operators use this skill to configure or adapt a Telegram-driven bot that evaluates Simmer weather markets with multiple forecast sources and a strict confidence threshold. It is intended for users who can review credentials, trading limits, and order controls before enabling live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot can place trades while some documented safety controls are missing or weaker than promised. <br>
Mitigation: Review and tighten trading controls before installation, including a real dry-run default or explicit live-trading opt-in, final confirmation before every order, restricted Telegram users, and true four-source numeric agreement. <br>
Risk: The skill depends on trading, weather, Telegram, and NVIDIA API credentials and external services. <br>
Mitigation: Disclose and scope all required credentials, use limited accounts or simulated venues where possible, and verify external service behavior before enabling automated execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrjoeteam/simmer-weather-trader) <br>
- [Skill instructions](SKILL.md) <br>
- [Bot README](simmer_weather_bot/README.md) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [NVIDIA FourcastNet API](https://climate.api.nvidia.com/v1/nvidia/fourcastnet) <br>
- [NOAA Weather API](https://api.weather.gov) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires external API credentials and review of trading controls before live use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
