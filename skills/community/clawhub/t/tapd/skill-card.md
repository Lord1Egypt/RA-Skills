## Description:

Tapd helps agents query, create, and update TAPD requirements, tasks, bugs, comments, workflows, iterations, test cases, wikis, timesheets, release plans, and WeCom notifications through the TAPD Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevindai](https://clawhub.ai/user/kevindai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and delivery teams use this skill to let an agent work with TAPD project-management data and WeCom notifications from authenticated API calls. It is intended for workflows that need TAPD item lookup, creation, updates, comments, workflow metadata, test cases, wikis, time entries, and release-plan information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send TAPD credentials to a configurable API host.

Mitigation: Use the official TAPD API or a vetted internal TAPD host, avoid plaintext HTTP, and control the runtime environment before installing.

Risk: The skill exposes broad read and write access to TAPD project data and WeCom webhook messages.

Mitigation: Use a short-lived, least-privilege TAPD token and require explicit confirmation before POST, batch, timesheet, wiki, relation, or webhook operations.

Risk: The security verdict requires review before operational use.

Mitigation: Install only when the publisher is trusted and the environment, credentials, and allowed endpoints are governed.

## Reference(s):

- [ClawHub Tapd skill page](https://clawhub.ai/kevindai/skills/tapd)
- [TAPD](https://www.tapd.cn)
- [TAPD API reference](reference/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON API responses, and inline shell or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include TAPD record links and structured API results; mutating actions should be reviewed before execution.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
