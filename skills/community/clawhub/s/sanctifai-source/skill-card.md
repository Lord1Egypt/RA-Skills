## Description:

SanctifAI Source lets AI agents request human review, approval, or task completion through REST API and MCP integration with asynchronous long-polling or webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sanctifai](https://clawhub.ai/user/sanctifai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to SanctifAI for human review, approval, task completion, worker discovery, file review, and feedback workflows. It is suited to agent workflows that need asynchronous human input through REST API calls, MCP tools, long-polling, or webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content and files may be sent to SanctifAI and, depending on routing, external human workers.

Mitigation: Use only content that is appropriate to share with SanctifAI and the selected workers; avoid public routing for confidential, personal, regulated, or credential-bearing material.

Risk: The skill can create tasks, upload files, share links, invite users, send billing invites, and mint another agent key.

Mitigation: Require explicit user or administrator approval before taking actions that create tasks, expose files or links, invite humans or agents, affect billing, or issue credentials.

Risk: MCP examples document bearer API keys in access_token URLs.

Mitigation: Treat MCP URLs containing access_token as secrets and prefer header-based authentication or secret-manager-backed configuration where available.

## Reference(s):

- [SanctifAI Source on ClawHub](https://clawhub.ai/sanctifai/skills/sanctifai-source)
- [SanctifAI public skill source](https://app.sanctifai.com/agents/source/skill.md)
- [SanctifAI API quick start](https://app.sanctifai.com/v1)
- [SanctifAI OpenAPI specification](https://app.sanctifai.com/v1/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, JavaScript, Python, curl, and MCP configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents in creating and managing third-party human-in-the-loop tasks; task results are returned by SanctifAI APIs, long-polling, or webhooks.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
