## Description:

Fetches current weather from Open-Meteo API and automatically captures a live webcam image from Meteoblue or Windy for the requested location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex1389](https://clawhub.ai/user/alex1389)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer weather questions with current Open-Meteo conditions and a live webcam image for the requested place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested locations may be sent to Open-Meteo, search providers, Meteoblue, Windy, or other webcam sites.

Mitigation: Avoid precise or sensitive location requests unless sharing them with those third-party services is acceptable.

Risk: The webcam browser session may retain cookies for visited webcam sites.

Mitigation: Use an isolated webcam browser session and clear its cookies or session state when retained browsing state is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alex1389/skills/weather-webcam-v2)
- [Publisher profile](https://clawhub.ai/user/alex1389)
- [Open-Meteo geocoding endpoint used by the skill](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo forecast endpoint used by the skill](https://api.open-meteo.com/v1/forecast)
- [Meteoblue webcam example: Roses](https://www.meteoblue.com/en/weather/webcams/roses_spain_3111348)
- [Meteoblue webcam example: Vilassar de Mar](https://www.meteoblue.com/en/weather/webcams/vilassar-de-mar_spain_3105522)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain-text or Markdown weather response with shell commands, JavaScript extraction snippets, and an optional downloaded webcam image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses requested location text to fetch weather data and locate a suitable public webcam page.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
