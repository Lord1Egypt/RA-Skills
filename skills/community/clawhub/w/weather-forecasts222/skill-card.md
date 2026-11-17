## Description:

Provides weather forecasts by city name, pinyin, coordinates, or IP-based auto-location, including current conditions, a three-day forecast, and condition icons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greenteawater](https://clawhub.ai/user/greenteawater)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to answer natural-language weather requests and return current conditions plus a simple three-day forecast with icons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather requests are sent to wttr.in, and empty-location requests may allow approximate location inference from network or IP information.

Mitigation: Use an explicit city or location when location inference is not desired, and disclose the external weather-service dependency before deployment.

Risk: Forecast content depends on wttr.in availability and accuracy.

Mitigation: Treat returned forecasts as informational, keep request failures visible to the user, and avoid using the output as a sole source for safety-critical decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/greenteawater/skills/weather-forecasts222)
- [ClawHub publisher profile](https://clawhub.ai/user/greenteawater)
- [wttr.in weather service](https://wttr.in/)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown-formatted weather report with current conditions, icon image links, and a three-day forecast.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and curl; no API key is required; queries wttr.in and can use IP-based location when no city is supplied.]

## Skill Version(s):

1.0.5555 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
