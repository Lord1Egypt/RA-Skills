## Description:

查询天气预报，支持城市名/坐标，提供当前天气和预报信息，包含图标展示。

This skill is ready for commercial/non-commercial use.

## Publisher:

[greenteawater](https://clawhub.ai/user/greenteawater)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer weather questions for a named city, coordinates, pinyin input, or IP-derived location. It returns current conditions and a short forecast with weather icons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries are sent to wttr.in, and when no city is supplied the service may infer location from the request IP.

Mitigation: Prefer explicit city or coordinate input when privacy matters, and disclose the external weather-service request path to users.

Risk: The script calls wttr.in without an explicit https:// URL and does not URL-encode city names.

Mitigation: Update the script to use an explicit https://wttr.in endpoint and URL-encode user-supplied locations before release hardening.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/greenteawater/skills/weather-forecasts)
- [wttr.in weather service](https://wttr.in)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown text with weather values and inline icon image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and curl; no API key is required.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
