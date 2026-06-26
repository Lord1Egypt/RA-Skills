## Description: <br>
Tianqi helps Chinese-speaking users get current weather and short-range forecasts for cities or regions using wttr.in and Open-Meteo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvy](https://clawhub.ai/user/jvy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users and agents use this skill to answer weather, temperature, rain, wind, and short-range forecast questions for a specified city or region, with clarification for ambiguous locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide exact private addresses or sensitive location descriptions when asking for weather. <br>
Mitigation: Ask for city-, district-, or region-level locations instead of exact private addresses. <br>
Risk: Plain HTTP or unstable location recognition can expose queries or produce the wrong forecast for ambiguous places. <br>
Mitigation: Prefer HTTPS weather service URLs and clarify ambiguous Chinese place names before answering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvy/tianqi) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=39.9042&longitude=116.4074&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum&forecast_days=3&timezone=auto) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Chinese-language plain text or Markdown with optional curl examples and weather data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Celsius by default and may identify wttr.in or Open-Meteo as the weather source when useful.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
