## Description: <br>
Get current weather conditions and forecasts for any location worldwide. Returns structured data with temperature, humidity, wind, precipitation, and more. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjtf93](https://clawhub.ai/user/pjtf93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to fetch current weather, forecasts, and location search results for trip planning, activity planning, and weather summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location queries are sent to external weather and geocoding providers. <br>
Mitigation: Avoid sending sensitive or unnecessary precise locations, and review provider behavior before commercial deployment. <br>
Risk: The install guidance fetches the upstream weathercli tool from GitHub. <br>
Mitigation: Review the upstream repository and use a pinned version or commit instead of @latest for stronger supply-chain control. <br>


## Reference(s): <br>
- [Weathercli GitHub releases](https://github.com/pjtf93/weathercli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; weathercli output is human-readable text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Location queries require network access to weather and geocoding providers; JSON output is recommended for parsing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
