## Description:

云效项目协作操作助手，支持工作项（任务、需求、缺陷）的查询、创建和更新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengerzh](https://clawhub.ai/user/fengerzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project collaborators use this skill to inspect Yunxiao projects and work item details, then create or update tasks, requirements, bugs, and related statuses through Yunxiao OpenAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent read/write Yunxiao tokens can expose sensitive or business-critical workspace data if config.json is shared or committed.

Mitigation: Use the narrowest token scope, keep config.json out of shared repositories and transcripts, restrict local file access, and rotate any token that may have been exposed.

Risk: Create, update, complete, or close operations can change live project data.

Mitigation: Require explicit user confirmation for write or status-changing actions and verify the target project and work item before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengerzh/skills/yunxiao)
- [Yunxiao OpenAPI base endpoint](https://openapi-rdc.aliyuncs.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local config.json containing Yunxiao organization, user, project, and token settings; write actions affect live Yunxiao data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
