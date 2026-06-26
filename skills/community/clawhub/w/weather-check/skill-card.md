## Description: <br>
Current weather conditions and multi-day forecasts for any location worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and external users use this skill to request current weather conditions and multi-day forecasts for global locations by name or coordinates through a disclosed weather API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather searches send location names or coordinates to weather.agentutil.net. <br>
Mitigation: Avoid sending sensitive, private, or regulated locations unless that disclosure is acceptable for the workspace. <br>
Risk: The skill documents free daily limits and an optional paid x402/USDC request flow. <br>
Mitigation: Use paid requests only when intentionally approved, and track query volume when operating near the free 10-query daily limit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CutTheMustard/weather-check) <br>
- [Weather API homepage](https://weather.agentutil.net) <br>
- [Current weather endpoint](https://weather.agentutil.net/v1/current) <br>
- [Forecast endpoint](https://weather.agentutil.net/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with curl examples and JSON API responses for current weather or forecasts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports location names or latitude and longitude coordinates; forecasts accept 1-16 days. Free use is documented as 10 queries per day, with an optional paid x402/USDC per-query flow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
