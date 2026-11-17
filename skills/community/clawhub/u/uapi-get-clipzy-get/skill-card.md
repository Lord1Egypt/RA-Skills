## Description:

使用 UAPI 的“步骤2 (方法一): 获取加密数据”单接口 skill，处理 步骤2 (方法一): 获取加密数据、加密剪贴板、端到端加密文本、加密分享 等请求。 Use when the user wants get clipzy get, api get, get, clipzy, or when you need to call GET /api/get directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve encrypted Clipzy clipboard data by ID through UAPI's GET /api/get endpoint, then handle client-side decryption with their own key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms such as "get" may cause an agent to select this skill for unrelated requests.

Mitigation: Invoke the skill explicitly by name or endpoint and confirm the user intends to use the Clipzy/UAPI encrypted data retrieval endpoint before proceeding.

Risk: Requests may include sensitive identifiers, API keys, or decryption-related material.

Mitigation: Review user-provided ids and credentials before sending them to UAPI, and keep decryption keys under the user's control.

Risk: The endpoint returns encrypted and compressed data, not final plaintext.

Mitigation: Make clear that the client must decrypt the response with the user's own key and verify that retrieving encrypted data is the desired intermediate step.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shuakami/skills/uapi-get-clipzy-get)
- [快速上手](references/quick-start.md)
- [步骤2 (方法一): 获取加密数据](references/operations/get-clipzy-get.md)
- [Clipzy 在线剪贴板 分类接口](references/resources/Clipzy-在线剪贴板.md)
- [UAPI](https://uapis.cn)
- [UAPI API Base URL](https://uapis.cn/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, API call instructions, Markdown]

**Output Format:** [Markdown with endpoint details, parameter requirements, response codes, and credential guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents a single GET endpoint that requires an id query parameter and returns encrypted, compressed data for client-side decryption.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
