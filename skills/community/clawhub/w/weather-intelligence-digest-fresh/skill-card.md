## Description: <br>
Generate daily Weather Intelligence Digest using NOAA/NWS data with customizable locations and alert monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyboy1241](https://clawhub.ai/user/dannyboy1241) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to generate daily weather briefings for configured locations, including short-term forecasts and active severe-weather alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured locations are sent to NOAA/NWS when forecasts and alerts are fetched. <br>
Mitigation: Only include locations you are comfortable sending to NOAA/NWS. <br>
Risk: Generated HTML can include text derived from configuration or API responses. <br>
Mitigation: Review or escape generated HTML before opening or publishing it when configuration or API content is untrusted. <br>
Risk: The dependency requirement allows newer requests versions, which can affect reproducibility. <br>
Mitigation: Install in a virtual environment and pin or review the requests version when reproducible execution matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dannyboy1241/weather-intelligence-digest-fresh) <br>
- [NOAA/NWS Weather API](https://api.weather.gov) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown, HTML, and JSON files with setup and execution commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured location names and coordinates; optional HTML output supports selectable themes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
