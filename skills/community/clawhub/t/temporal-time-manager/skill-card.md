## Description:

Temporal Time Manager lets an AI assistant manage tasks, schedules, and captured ideas through conversation, syncing data to aitimemg.cn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangkaifeng](https://clawhub.ai/user/pangkaifeng)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent list, create, update, and delete tasks and schedules, and capture ideas in an aitimemg.cn account.

### Deployment Geography for Use:

Global; service data is stored on Alibaba Cloud in Mainland China per skill metadata.

## Known Risks and Mitigations:

Risk: The skill can permanently change or delete synced task and schedule data.

Mitigation: Require the agent to confirm exact task or schedule IDs and names before any update or deletion.

Risk: Use requires API-token access to aitimemg.cn task data.

Mitigation: Install only when the user accepts token-based access to that data, and keep TEMPORAL_API_TOKEN scoped and protected.

## Reference(s):

- [Temporal Time Manager on ClawHub](https://clawhub.ai/pangkaifeng/skills/temporal-time-manager)
- [Publisher profile](https://clawhub.ai/user/pangkaifeng)
- [aitimemg.cn](https://www.aitimemg.cn)
- [aitimemg.cn settings](https://www.aitimemg.cn/settings)
- [Temporal Time Manager API server](https://api.aitimemg.cn)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown or text responses with OpenAPI-backed tool calls and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEMPORAL_API_TOKEN and optionally TEMPORAL_BASE_URL; API responses are JSON.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
