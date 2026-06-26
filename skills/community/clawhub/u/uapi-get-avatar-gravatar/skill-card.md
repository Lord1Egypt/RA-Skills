## Description: <br>
使用 UAPI 的“获取Gravatar头像”单接口 skill，处理 获取Gravatar头像、头像获取 等请求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to decide when and how to call UAPI's GET /avatar/gravatar endpoint for Gravatar avatar lookup. It helps confirm required email or hash inputs, optional image parameters, authentication fallback, and common response codes before making the API request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email addresses or Gravatar hashes submitted to the endpoint are personal data sent to an external service. <br>
Mitigation: Prefer a precomputed lowercase MD5 Gravatar hash when possible and avoid sending raw email addresses unless needed. <br>
Risk: Anonymous or free-tier UAPI requests may hit quota limits or require authentication. <br>
Mitigation: When the endpoint returns 429 or a quota-related error, use a UAPI account key and retry within the service's limits. <br>
Risk: Incomplete requests fail when neither email nor hash is supplied. <br>
Mitigation: Confirm that either email or hash is present before calling GET /avatar/gravatar. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/uapi-get-avatar-gravatar) <br>
- [Quick Start](references/quick-start.md) <br>
- [获取Gravatar头像](references/operations/get-avatar-gravatar.md) <br>
- [Image 分类接口](references/resources/Image.md) <br>
- [UAPI base URL](https://uapis.cn/api/v1) <br>
- [UAPI registration](https://uapis.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with endpoint details and request parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce endpoint selection guidance, query parameter recommendations, authentication fallback advice, and response-code handling notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
