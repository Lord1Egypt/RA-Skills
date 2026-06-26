## Description: <br>
小红书矩阵系统 API 调用工具，集成红薯矩阵平台（hongshujuzhen.com）。支持：搜索小红书笔记、获取笔记详情、发布图文笔记、查询账号列表、查询 API 使用统计、批量管理小红书账号。触发词：小红书、xhs、笔记搜索、发布小红书、API 调用、红薯矩阵。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[admin6016](https://clawhub.ai/user/admin6016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to connect an agent to the Hongshu Matrix API for Xiaohongshu note search, note detail retrieval, account lookup, usage reporting, and image note publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents credentialed HTTP API calls for account access and public publishing. <br>
Mitigation: Use HTTPS where available, avoid placing API keys in URLs, and keep credentials revocable and scoped to the minimum privileges needed. <br>
Risk: The publish endpoint can create or schedule public Xiaohongshu content. <br>
Mitigation: Require explicit user approval after showing the exact account, title, content, images, topics, and schedule before any publish request. <br>
Risk: The API provider is a third-party RedAPI service. <br>
Mitigation: Install and use the skill only when the operator trusts the RedAPI provider and has confirmed the service terms and data handling expectations. <br>


## Reference(s): <br>
- [小红书矩阵系统 API 文档](references/api.md) <br>
- [红薯矩阵平台](https://hongshujuzhen.com) <br>
- [RedAPI base endpoint](http://redapi.cn) <br>
- [ClawHub skill page](https://clawhub.ai/admin6016/xhsmatrixmanager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with Python requests snippets and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided RedAPI API key and account-specific publish inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
