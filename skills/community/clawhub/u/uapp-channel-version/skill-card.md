## Description: <br>
友盟 U-App 渠道/版本分析技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 5 个只读查询接口，涵盖渠道/版本单日快照与渠道/版本的启动次数、活跃用户、新增用户趋势分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analytics operators use this skill to query read-only Umeng U-App channel and version metrics, compare daily channel or version performance, and analyze launches, active users, and new-user trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill instructs agents to send appkeys to a separate tracing command before analytics calls. <br>
Mitigation: Treat appkeys as sensitive operational identifiers, avoid production appkeys until tracing behavior is removed or made explicitly user-controlled, and ask the publisher for telemetry disclosure and an opt-out path. <br>
Risk: The skill requires Umeng credentials and appkeys to access analytics data. <br>
Mitigation: Use least-privilege accounts where possible, verify login state with umeng-cli, and avoid exposing appkeys in shared logs or public transcripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/squall0925/uapp-channel-version) <br>
- [umeng-cli Project Homepage](https://github.com/umeng/umeng-cli) <br>
- [Umeng Website](https://www.umeng.com/) <br>
- [Umeng OpenAPI Gateway](https://gateway.open.umeng.com/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the umeng-cli binary and Umeng login credentials; queries are read-only but require an appkey.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
