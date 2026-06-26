## Description: <br>
Provides weather information for a user's location and requested date by consulting weather websites through a browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uwvwko-zzz](https://clawhub.ai/user/uwvwko-zzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to answer current or near-future weather questions for a city, including temperature, conditions, wind, humidity, air quality, and severe-weather notes when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location lookup may disclose location-related data to third-party IP geolocation or weather websites when the city is not provided. <br>
Mitigation: Ask the user for the city directly and avoid IP-based location lookup when the location is sensitive. <br>
Risk: Weather reports can be stale or incomplete if a selected weather source is unavailable or not current. <br>
Mitigation: Use the latest available data, try the documented fallback weather sites, and call out severe-weather alerts when source pages provide them. <br>


## Reference(s): <br>
- [China Weather](https://www.weather.com.cn) <br>
- [Moji Weather](https://www.moji.com) <br>
- [National Meteorological Center](https://nmc.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown weather report with browser command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use user-provided location, chat history, or IP-based location lookup to select the weather source query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
