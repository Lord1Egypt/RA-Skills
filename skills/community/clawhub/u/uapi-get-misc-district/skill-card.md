## Description:

使用 UAPI 的“Adcode 国内外行政区域查询”接口帮助代理查询国内外行政区域、行政编码和坐标反查结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user needs UAPI administrative district lookup through GET /misc/district, including keyword search, adcode lookup, or coordinate reverse lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative-region search terms, adcodes, or coordinates may be sent to UAPI when the skill is invoked.

Mitigation: Use the skill only for explicit administrative district lookup tasks and avoid sending unnecessary precise coordinates or sensitive location details.

Risk: The broad district trigger could select this skill when another district-related task was intended.

Mitigation: Confirm that the user needs UAPI administrative district lookup before preparing the API call.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [Adcode 国内外行政区域查询](references/operations/get-misc-district.md)
- [Misc 分类接口](references/resources/Misc.md)
- [UAPI](https://uapis.cn)
- [UAPI API Base URL](https://uapis.cn/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with endpoint, parameter, authentication, and response-code details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare GET /misc/district requests using keywords, adcode, or latitude and longitude query parameters.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
