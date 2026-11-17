## Description:

Current Weather helps an agent identify the user's city and requested date, look up current or near-term weather from web sources, and return a concise forecast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uwvwko-zzz](https://clawhub.ai/user/uwvwko-zzz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and assistants use this skill to answer weather questions for today, tomorrow, later days, or multi-day periods by collecting a city and checking weather websites.

### Deployment Geography for Use:

Global; source examples and city codes focus on China.

## Known Risks and Mitigations:

Risk: The agent may infer a user's city through third-party IP lookup without clear consent.

Mitigation: Ask the user for their city first; use IP geolocation only after explicit opt-in and confirm any inferred city before querying weather sources.

Risk: Weather information is time-sensitive and may be incomplete or stale when pulled from public web pages.

Mitigation: Include the date and source context in the response, and direct users to official meteorological alerts for severe or safety-critical weather decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uwvwko-zzz/skills/uwvwko-current-weather)
- [Publisher profile](https://clawhub.ai/user/uwvwko-zzz)
- [China Weather](https://www.weather.com.cn)
- [Moji Weather](https://www.moji.com)
- [National Meteorological Center](https://nmc.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise natural-language weather report, optionally with structured markdown fields and browser command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include date, city, temperature range, weather condition, wind, humidity, air quality, and extreme-weather notes when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
