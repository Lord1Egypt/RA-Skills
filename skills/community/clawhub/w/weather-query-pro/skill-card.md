## Description: <br>
China Weather helps agents answer Chinese city weather queries with current conditions, forecasts, air quality, life indices, and fallback weather APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query weather for Chinese cities and receive formatted current weather, forecasts, air quality, and life-index guidance through configured or no-key weather APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City names are sent to third-party weather API providers during lookups. <br>
Mitigation: Use the no-key wttr.in path where acceptable and avoid submitting sensitive location context beyond the city needed for the query. <br>
Risk: Configured QWeather, OpenWeatherMap, or Seniverse API keys could be exposed if copied into shared logs, prompts, or configuration files. <br>
Mitigation: Store keys in environment variables, restrict access to shared execution logs, and rotate any key that may have been disclosed. <br>
Risk: The skill may ask the agent environment to install Python dependencies before running weather queries. <br>
Mitigation: Use a trusted Python environment or virtual environment for dependency installation before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/weather-query-pro) <br>
- [QWeather developer documentation](https://dev.qweather.com) <br>
- [OpenWeatherMap API documentation](https://openweathermap.org/api) <br>
- [Seniverse weather API](https://www.seniverse.com) <br>
- [wttr.in weather service](https://wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with formatted weather reports and inline Python or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API setup steps and weather data sourced from wttr.in, QWeather, OpenWeatherMap, or Seniverse.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
