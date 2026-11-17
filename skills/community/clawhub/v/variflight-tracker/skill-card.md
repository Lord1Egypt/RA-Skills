## Description:

基于飞常准数据，提供航班实时动态、延误分析、舒适度评分、机场天气查询，覆盖全球航班，零配置即用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to check flight status, route-level delays, airport weather, and comfort comparisons from flight numbers, city pairs, dates, or airport names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight numbers, routes, dates, and airport/weather queries are sent to an external proxy service.

Mitigation: Use the skill only when that data flow is acceptable for the user or organization.

Risk: The skill requires PROXY_TOKEN even though the description says it is zero-configuration.

Mitigation: Configure PROXY_TOKEN as a secret and avoid exposing it in prompts, logs, or shared files.

Risk: Broad airport and weather trigger patterns may activate the skill more often than expected.

Mitigation: Review the intended query before invoking the tool and ask for clarification when the user request is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/variflight-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/travel-skills)
- [External flight-data proxy endpoint](https://1439498936-eqcpuaevzz.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, API calls, guidance]

**Output Format:** [Markdown summaries and JSON status/error payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tables, status labels, delay analysis, comfort scores, and airport weather impact notes.]

## Skill Version(s):

1.1.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
