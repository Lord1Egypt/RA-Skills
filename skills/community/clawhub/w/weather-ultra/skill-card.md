## Description: <br>
Queries weather, air quality, sunrise and sunset times, Golden Hour and Blue Hour windows, and sunrise or sunset color quality for photography and outdoor planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pazzilivo](https://clawhub.ai/user/Pazzilivo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, photographers, outdoor planners, and agents use this skill to fetch weather, air quality, sun events, Golden Hour and Blue Hour timing, and sunrise or sunset quality for a requested city. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried city and derived coordinates are sent to external WeatherAPI and SunsetHue services. <br>
Mitigation: Use the skill only when sharing queried locations with those services is acceptable. <br>
Risk: The skill reads local API keys from ~/.openclaw/.env. <br>
Mitigation: Keep the environment file trusted and use limited-purpose WeatherAPI and SunsetHue keys. <br>
Risk: The script depends on local curl and jq commands being available. <br>
Mitigation: Confirm curl and jq are installed before running the skill. <br>


## Reference(s): <br>
- [Weather Ultra ClawHub release](https://clawhub.ai/Pazzilivo/weather-ultra) <br>
- [WeatherAPI forecast request used by the skill](https://api.weatherapi.com/v1/forecast.json?key=${WEATHERAPI_KEY}&q=${CITY}&days=${DAYS}&lang=zh&aqi=yes) <br>
- [SunsetHue sunrise forecast request used by the skill](https://api.sunsethue.com/event?latitude=${LAT}&longitude=${LON}&date=${DATE}&type=sunrise&key=${SUNSETHUE_KEY}) <br>
- [SunsetHue sunset forecast request used by the skill](https://api.sunsethue.com/event?latitude=${LAT}&longitude=${LON}&date=${DATE}&type=sunset&key=${SUNSETHUE_KEY}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text weather and photography-light forecast report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires city input and optional day count; uses WeatherAPI and SunsetHue API keys from the local OpenClaw environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
