## Description:

基于 Todoist 的任务可见性管理，用于创建、更新和追踪任务状态，并记录进度评论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[near2sea](https://clawhub.ai/user/near2sea)

### License/Terms of Use:


## Use Case:

Developers and Todoist users use this skill to manage Todoist task visibility from an agent workflow, including creating tasks, moving tasks between in-progress, waiting, and done sections, and adding progress comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Todoist API token gives the scripts broad authority to read and modify Todoist resources.

Mitigation: Use a dedicated Todoist token where possible, keep token configuration private with restrictive permissions, and review each write action before execution.

Risk: Untrusted task JSON or comment text can be passed directly into shell scripts that send Todoist write requests.

Mitigation: Avoid passing untrusted text into task JSON or comment arguments, and inspect generated payloads before running create, update, or comment commands.

## Reference(s):

- [Todoist Developer Settings](https://todoist.com/app/settings/integrations/developer)
- [Todoist REST API v2](https://api.todoist.com/rest/v2)
- [Todoist API v1](https://api.todoist.com/api/v1)
- [ClawHub skill page](https://clawhub.ai/near2sea/skills/todoist-visibility)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq with Todoist token, project, and section environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
