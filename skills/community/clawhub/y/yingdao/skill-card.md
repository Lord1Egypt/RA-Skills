## Description: <br>
影刀 RPA API 封装，支持鉴权/任务查询/执行/结果获取。需配置环境变量 YINGDAO_ACCESS_KEY_ID、YINGDAO_ACCESS_KEY_SECRET 作为 API 凭证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yflmq001](https://clawhub.ai/user/yflmq001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to connect agents to Yingdao RPA APIs for authentication, task discovery, task execution, and execution-result retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start real remote Yingdao RPA automation jobs when valid account credentials are available. <br>
Mitigation: Use limited-scope or test credentials, require manual approval before task starts, and restrict which task UUIDs the agent may run. <br>
Risk: The artifact does not provide built-in execution guardrails or independently verifiable duplicate-run protection. <br>
Mitigation: Add or verify duplicate-run protection before relying on idempotent execution behavior in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yflmq001/yingdao) <br>
- [Yingdao authentication API endpoint](https://api.yingdao.com/oapi/token/v2/token/create) <br>
- [Yingdao business API base](https://api.winrobot360.com/oapi) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and JSON API payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YINGDAO_ACCESS_KEY_ID and YINGDAO_ACCESS_KEY_SECRET environment variables and the requests Python dependency.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
