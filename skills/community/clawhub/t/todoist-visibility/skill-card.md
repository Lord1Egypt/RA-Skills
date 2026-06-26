## Description: <br>
基于 Todoist 的任务可见性管理。用于创建、更新和追踪任务状态（进行中🟡、等待中🟠、已完成🟢），并记录进度评论。当用户提到 Todoist 任务管理、任务状态追踪、或需要使用 Todoist API 时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[near2sea](https://clawhub.ai/user/near2sea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Todoist users use this skill to create, update, query, and track Todoist tasks across in-progress, waiting, and completed sections while adding progress comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authenticated access to read and modify Todoist account data. <br>
Mitigation: Install only when that access is acceptable, use a protected secret store or private shell config for TODOIST_TOKEN, and avoid exposing the token in shared logs, screenshots, or repositories. <br>
Risk: The generic Todoist API wrapper can perform broad Todoist operations with limited built-in scoping or confirmation. <br>
Mitigation: Add confirmation before write actions and limit or remove generic API-wrapper use when a narrower task workflow is sufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/near2sea/todoist-visibility) <br>
- [Todoist developer settings](https://todoist.com/app/settings/integrations/developer) <br>
- [Todoist REST API v1 endpoint](https://api.todoist.com/api/v1) <br>
- [Todoist REST API v2 comments endpoint](https://api.todoist.com/rest/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, a Todoist API token, a Todoist project ID, and configured section IDs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
