## Description: <br>
Qweather helps agents query QWeather for current weather, forecasts, warnings, air quality, and weather-related indices by city code, city name, or coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k176060444-lgtm](https://clawhub.ai/user/k176060444-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user explicitly requests QWeather-backed weather data or needs free API weather lookup. It is intended for weather, forecast, air quality, warning, and lifestyle-index responses using QWeather inputs such as city codes, city names, or coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested city codes, city names, or coordinates to QWeather through a publisher-provided shared API key. <br>
Mitigation: Install only when this data sharing is acceptable; prefer a version that lets users configure their own QWeather host and API key. <br>
Risk: The shared free API key has request limits and service restrictions that may affect reliability or permitted use. <br>
Mitigation: Confirm QWeather terms and quota needs before production use, and replace the shared key with an organization-controlled credential where possible. <br>
Risk: The security guidance notes that some advertised features may need cleanup. <br>
Mitigation: Test each weather endpoint needed for deployment before relying on the skill in user-facing workflows. <br>


## Reference(s): <br>
- [QWeather Geo API documentation](https://dev.qweather.com/docs/api/geo/) <br>
- [ClawHub skill page](https://clawhub.ai/k176060444-lgtm/qweather-cn) <br>
- [Publisher profile](https://clawhub.ai/user/k176060444-lgtm) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Weather results are returned from QWeather API responses and may require QWeather attribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
