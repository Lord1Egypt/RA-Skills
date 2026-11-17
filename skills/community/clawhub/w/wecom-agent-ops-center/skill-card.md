## Description:

企微 AI Agent 可观测性工具 — 心跳监控、进程守护、敏感信息扫描、网络白名单，2 分钟接入

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeliang2000](https://clawhub.ai/user/mikeliang2000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and teams running WorkBuddy or OpenClaw AI agents use this skill to monitor agent health, receive WeCom alerts, track tasks and resources, and configure process, secrets, and network guards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud conversion and scanner registration may transmit enterprise chat content, Agent metadata, user or tenant identifiers, and process command fragments to an external service.

Mitigation: Review data flows before installation, disable cloud conversion and daemon scanning unless required, and restrict external transmission to approved environments.

Risk: Dashboard, lifecycle, and notification APIs expose powerful management controls.

Mitigation: Keep the dashboard bound to localhost or place it behind real authentication, and avoid exposing lifecycle or notification APIs publicly.

Risk: Secret scanning may detect sensitive values that could be mishandled in logs or alerts.

Mitigation: Ensure secret findings are redacted or blocked and are not written to logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikeliang2000/skills/wecom-agent-ops-center)
- [Publisher profile](https://clawhub.ai/user/mikeliang2000)
- [HermesAI homepage](https://hermesai.ltd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local dashboard endpoints, WeCom credentials, cloud conversion settings, and agent monitoring configuration.]

## Skill Version(s):

2.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
