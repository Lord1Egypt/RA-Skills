## Description:

通过17位车架号（VIN码）查询车辆信息，包括品牌、车型年款、排量、发动机类型及指导价等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external vehicle-information workflows use this skill to query TianAPI with a 17-character VIN and return vehicle details for identification, used-car checks, and information verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried VINs are shared with TianAPI during lookup.

Mitigation: Use the skill only when sharing the VIN with TianAPI is acceptable for the workflow.

Risk: API keys can be exposed through command-line arguments, key-bearing URLs, logs, tickets, or a local scripts/.env file.

Mitigation: Prefer TIANAPI_VIN_KEY, avoid copying full key-bearing URLs into logs or tickets, and protect or omit scripts/.env.

## Reference(s):

- [TianAPI VIN Query API documentation](https://www.tianapi.com/apiview/260)
- [TianAPI VIN query endpoint](https://apis.tianapi.com/chavin/index)
- [ClawHub skill release](https://clawhub.ai/workxin/skills/tianapi-vin-query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TianAPI API key and a 17-character VIN; queried VINs are sent to TianAPI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
