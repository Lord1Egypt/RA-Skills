## Description:

全球地点天气预报及地理编码分析（TJWeather API）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiansonguio](https://clawhub.ai/user/qiansonguio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to resolve global place names, retrieve TJWeather forecasts, and produce concise weather summaries with matched-location context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries are sent to external geocoding services, and coordinates plus the TJWeather API key are sent to TJWeather.

Mitigation: Use only with locations appropriate for those external services, disclose this data flow where relevant, and provide the API key through SecretRef or an environment variable.

Risk: The documentation includes plaintext credential examples and shared trial keys.

Mitigation: Use a private TJWeather API key, avoid plaintext configuration for deployed environments, and do not rely on the shared trial keys.

Risk: Ambiguous places may fall back to city-level or fuzzy geocoding, which can reduce forecast precision.

Mitigation: Show the matched location and fallback status in the first response line, and ask for a more precise location or coordinates when the match is uncertain.

Risk: Forecasts beyond the supported window and daylight-saving-time assumptions can produce misleading timelines.

Mitigation: Limit requests to the supported 10-day forecast window, tell the user when truncation occurs, and verify the local DST offset before calling the weather script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiansonguio/skills/tjweather)
- [TJWeather API homepage](https://api.tjweather.com)
- [TJWeather official website](https://www.tjweather.com/)
- [TJWeather API key application](https://www.tjweather.com/Apply)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with weather statistics, matched-location notice, and summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are primarily Chinese and should include the query match, daily forecast statistics, and a brief user-facing summary.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
