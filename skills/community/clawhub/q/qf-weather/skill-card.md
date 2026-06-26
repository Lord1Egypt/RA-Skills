## Description: <br>
Provides real-time weather, hourly forecasts, and 7-day forecasts by city name, coordinates, or IP location without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[371166758-qq](https://clawhub.ai/user/371166758-qq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to look up current weather and short-term forecasts for a city, coordinate pair, or IP-derived location without configuring a weather API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries may disclose city names, coordinates, or IP-derived location to external weather providers. <br>
Mitigation: Prefer city-name queries when precise coordinates or IP-based location are not needed. <br>
Risk: External weather providers can be slow, unavailable, or return provider-specific results. <br>
Mitigation: Use the documented fallback behavior and treat weather output as current provider-sourced data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/371166758-qq/qf-weather) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash examples and weather summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses external weather providers and does not require an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
