## Description: <br>
Queries the QWeather API for current weather, hourly and daily forecasts, air quality, and alerts for cities in China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[royalmetoo](https://clawhub.ai/user/royalmetoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve QWeather-backed weather reports, forecasts, air quality, and alerts for Chinese cities after configuring a QWeather API host and key. <br>

### Deployment Geography for Use: <br>
Global use; weather lookup is limited to cities in China. <br>

## Known Risks and Mitigations: <br>
Risk: The QWeather API key can be exposed through the local config file, request URLs, logs, or shared transcripts. <br>
Mitigation: Keep qweather_config.json private, avoid sharing transcripts or logs that include request URLs, and rotate the key if exposure is suspected. <br>
Risk: Weather responses depend on a valid QWeather API host and key and may be unavailable when configuration or API calls fail. <br>
Mitigation: Check api_host and api_key before use, use the official QWeather console values, and report configuration or API failures without inventing weather data. <br>


## Reference(s): <br>
- [QWeather API reference](artifact/references/api_reference.md) <br>
- [QWeather console](https://console.qweather.com) <br>
- [ClawHub skill page](https://clawhub.ai/royalmetoo/qweather-query) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/royalmetoo) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown weather summaries with structured fields and source attribution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided QWeather API host and key; omits unavailable fields instead of fabricating data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
