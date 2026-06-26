## Description: <br>
管理无阶未来GPU云平台实例的创建、查询与删除操作；当用户需要创建GPU容器、查询实例状态、获取应用app_id或清理资源时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luckiehao](https://clawhub.ai/user/luckiehao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Vylai GPU cloud instances, including discovering app and GPU IDs, creating GPU containers, checking instance status, and deleting resources when work is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create GPU cloud resources that may incur account cost. <br>
Mitigation: Use a least-privileged Vylai API token and confirm app_id, gpu_id, gpu_num, and task_id before running creation commands. <br>
Risk: The skill can delete Vylai instances by task_id or deploy_name. <br>
Mitigation: Confirm the exact task_id or deploy_name before deletion, and query instance status first when there is any uncertainty. <br>
Risk: The Vylai API token grants access to private account resources. <br>
Mitigation: Provide the token through environment variables only, avoid logging or sharing shell history that exposes it, and use --no-token when only public app listings are needed. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [Vylai Platform](https://vylai.com) <br>
- [Vylai API Console](https://vylai.com/console/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/luckiehao/vylai-instance-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses authenticated Vylai API calls for private account operations; public app listing can run without a token.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
