## Description:

使用 UAPI 的 GET /misc/weather 接口查询实时天气、城市天气、行政区天气和可选预报数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to decide when and how to call UAPI's GET /misc/weather endpoint for weather lookup by city, adcode, or IP-derived location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather lookups contact the external UAPI service.

Mitigation: Tell users that requests are sent to uapis.cn before using the endpoint.

Risk: If city and adcode are omitted, the service may infer location from the client IP.

Mitigation: Prefer an explicit city or adcode when the user wants control over location disclosure.

Risk: Adding a UAPI Key links requests to a service account.

Mitigation: Use a UAPI Key only when the user accepts that service-account use, such as after anonymous quota is exhausted.

## Reference(s):

- [Quick Start](artifact/references/quick-start.md)
- [GET /misc/weather Operation Reference](artifact/references/operations/get-misc-weather.md)
- [Misc Resource Reference](artifact/references/resources/Misc.md)
- [UAPI Service](https://uapis.cn)
- [UAPI API Base URL](https://uapis.cn/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, API call guidance, configuration]

**Output Format:** [Markdown guidance with endpoint, parameter, authentication, and response-code details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include city, adcode, lang, extended, forecast, hourly, minutely, and indices query parameters.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
