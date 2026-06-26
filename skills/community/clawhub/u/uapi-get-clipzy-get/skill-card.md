## Description: <br>
使用 UAPI 的“步骤2 (方法一): 获取加密数据”单接口 skill，处理 步骤2 (方法一): 获取加密数据、加密剪贴板、端到端加密文本、加密分享 等请求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuakami](https://clawhub.ai/user/shuakami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to decide when to call the UAPI Clipzy `GET /api/get` endpoint, confirm the required `id` query parameter, and interpret the documented success and error responses for encrypted clipboard retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording such as "get" could route unrelated requests to this skill. <br>
Mitigation: Use it only when the user explicitly provides or requests a Clipzy/UAPI retrieval flow and an appropriate Clipzy id. <br>
Risk: A UAPI Key may consume account quota if supplied unnecessarily. <br>
Mitigation: Provide a UAPI Key only when account access is intended or quota-related errors require authenticated retry. <br>
Risk: The endpoint returns encrypted data and does not perform client-side decryption. <br>
Mitigation: Keep decryption keys outside the skill and decrypt only in the user's trusted client workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shuakami/uapi-get-clipzy-get) <br>
- [UAPI base URL](https://uapis.cn/api/v1) <br>
- [UAPI account site](https://uapis.cn) <br>
- [快速上手](references/quick-start.md) <br>
- [步骤2 (方法一): 获取加密数据](references/operations/get-clipzy-get.md) <br>
- [Clipzy 在线剪贴板 分类接口](references/resources/Clipzy-在线剪贴板.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with endpoint, parameter, authentication, and response-code details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend a UAPI Key only when quota or account-related errors indicate it is needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
