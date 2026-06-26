## Description: <br>
Uses UAPI's Answer Book endpoint to help agents prepare or perform GET /answerbook/ask requests for entertainment-style question answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when a conversation specifically requires the UAPI Answer Book API. It helps confirm the required question parameter, request path, authentication posture, quota handling, and expected response codes before using the endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad ask trigger could activate for generic requests. <br>
Mitigation: Invoke the skill only when the user explicitly wants UAPI Answer Book behavior or GET /answerbook/ask. <br>
Risk: Questions are sent to uapis.cn and may contain sensitive information. <br>
Mitigation: Do not include private, confidential, or regulated information in the question parameter. <br>
Risk: Anonymous quota may be exhausted and return 429. <br>
Mitigation: Use only a UAPI-specific key if quota limits require one. <br>


## Reference(s): <br>
- [UAPI 答案之书 接口 on ClawHub](https://clawhub.ai/shuakami/uapi-get-answerbook-ask) <br>
- [Quick Start](references/quick-start.md) <br>
- [答案之书](references/operations/get-answerbook-ask.md) <br>
- [Random 分类接口](references/resources/Random.md) <br>
- [UAPI](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API calls] <br>
**Output Format:** [Markdown guidance with endpoint details, request parameters, and response-code notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a non-empty question query parameter; avoid private information in questions sent to uapis.cn.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
