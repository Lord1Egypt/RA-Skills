## Description:

使用 UAPI 的“时间戳转换”单接口 skill，帮助代理调用 GET /convert/unixtime 在 Unix 时间戳和日期字符串之间转换。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user needs UAPI timestamp conversion through GET /convert/unixtime, including converting 10- or 13-digit Unix timestamps to dates or standard date strings to Unix timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send a user-provided timestamp or date string to an external UAPI service.

Mitigation: Avoid submitting sensitive or confidential values unless external API use is acceptable for the task.

Risk: Anonymous UAPI quota can be exhausted, which may require a UAPI key to continue.

Mitigation: Use a UAPI key only when needed and handle quota-related errors before retrying.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [GET /convert/unixtime Operation](references/operations/get-convert-unixtime.md)
- [Convert Resource](references/resources/Convert.md)
- [UAPI API Base](https://uapis.cn/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/shuakami/skills/uapi-get-convert-unixtime)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown guidance with API endpoint, parameters, and response handling details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external UAPI service with the timestamp or date string supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
