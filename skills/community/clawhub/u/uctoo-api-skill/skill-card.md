## Description: <br>
完整的 uctoo 后端 API 集成技能。将自然语言请求转换为 uctoo-backend API 调用，支持用户管理、产品管理、订单管理、登录认证等功能。使用时用户提及 "uctoo"、"后端API"、"用户管理"、"产品"、"订单"、"登录"、"认证" 等关键词时，你应该直接使用 http_request 工具发起实际的 API 请求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UCTooCom](https://clawhub.ai/user/UCTooCom) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to turn natural-language requests into authenticated UCTOO backend API calls for login, user management, product management, order management, and entity CRUD workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated API actions can create, update, delete, bulk edit, or force-delete UCTOO records from broad natural-language requests. <br>
Mitigation: Require the agent to show the exact endpoint, request body, and target record before executing create, update, delete, bulk, or force-delete actions. <br>
Risk: Credentials, access tokens, request bodies, and API responses may appear in chat logs or tool output. <br>
Mitigation: Use limited-permission accounts and avoid production credentials unless the environment protects chat logs and tool output. <br>
Risk: The skill depends on trust in the live UCTOO backend and its authorization behavior. <br>
Mitigation: Install only after confirming the target UCTOO backend and account permissions are appropriate for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/UCTooCom/uctoo-api-skill) <br>
- [Publisher profile](https://clawhub.ai/user/UCTooCom) <br>
- [Uctoo API Spec](references/api_spec.md) <br>
- [Usage Examples](references/examples.md) <br>
- [UCTOO API Design](references/uctoo_api_design.md) <br>
- [UCTOO backend API](https://javatoarktsapi.uctoo.com) <br>
- [Apifox API documentation](https://apifox.com/apidoc/shared/9a22079c-a59f-4b65-a7f6-678f0643e7f6/api-170720939) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON request examples and API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue authenticated create, update, delete, bulk, or force-delete API requests through the agent's HTTP request tool.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata; artifact metadata declares 7.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
