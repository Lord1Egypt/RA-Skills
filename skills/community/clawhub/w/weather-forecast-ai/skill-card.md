## Description: <br>
Helps agents answer current weather and forecast questions for a location using wttr.in or Open-Meteo, without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check current conditions, rain chances, temperatures, and short forecasts for cities, regions, or airport codes during everyday or travel-planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to a public weather service. <br>
Mitigation: Use coarse locations such as a city or airport code, and avoid exact private addresses or sensitive travel details unless needed. <br>
Risk: The skill depends on curl and remote weather service availability. <br>
Mitigation: Confirm curl is available before use and treat service errors, rate limits, or unavailable forecasts as non-authoritative results. <br>
Risk: The artifact does not support severe weather alerts, historical weather, or specialized aviation and marine weather. <br>
Mitigation: Use official or specialized weather sources for alerts, historical analysis, aviation, marine, or other high-stakes forecasts. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [ClawHub Weather skill](https://clawhub.ai/utromaya-code/weather-forecast-ai) <br>
- [Publisher profile](https://clawhub.ai/user/utromaya-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and weather query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return wttr.in text, JSON, or PNG weather responses depending on the command format selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
