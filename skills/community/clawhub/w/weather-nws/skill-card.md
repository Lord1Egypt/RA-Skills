## Description: <br>
Provides US weather forecasts via the National Weather Service with detailed accumulation data, watches and warnings, actionable timing, and automatic wttr.in fallback for non-US locations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patelhiren](https://clawhub.ai/user/patelhiren) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer weather questions for US locations with NWS forecasts, alerts, accumulations, observations, air quality, aviation, astronomy, and fire-weather context, with a less detailed global fallback for non-US locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried locations may include home addresses or travel plans and are sent to public geocoding and weather providers. <br>
Mitigation: Use coarse locations when possible and avoid submitting sensitive personal locations unless the user accepts that disclosure. <br>
Risk: Optional AQI lookup uses an AirNow API key. <br>
Mitigation: Use a dedicated AirNow key for this skill and do not reuse sensitive credentials. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/patelhiren/weather-nws) <br>
- [National Weather Service API](https://api.weather.gov/) <br>
- [AirNow API account request](https://docs.airnowapi.org/account/request/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted weather report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include forecast timing, weather alerts, accumulation estimates, AQI guidance, observed conditions, astronomical times, aviation forecasts, or fire-weather information depending on requested flags.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
