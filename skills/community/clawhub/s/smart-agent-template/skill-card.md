## Description:

Smart Agent Template provides an agent workflow template for task triage, WBS-style decomposition, context management, memory practices, reporting standards, and optional bot integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whhaijun](https://clawhub.ai/user/whhaijun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give AI agents a reusable operating method for decomposing complex work, controlling context growth, maintaining lightweight memory, reporting progress, and coordinating multi-agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Startup auto-update behavior can fetch and apply remote changes before the user reviews them.

Mitigation: Review the configured remote and branch, then disable startup auto-update unless automatic pulls are explicitly required.

Risk: The artifact includes TLS-verification bypass and SDK rewriting behavior in the optional Feishu startup flow.

Mitigation: Remove TLS bypasses, avoid modifying installed SDK files, and use normal certificate validation before deploying the integration.

Risk: Webhook and bot integrations can receive external messages and use credentials or verification tokens.

Mitigation: Require authenticated bot/webhook access, configure required secrets, and avoid running with empty verification tokens outside local testing.

Risk: Local memory and task files are keyed by user or chat identifiers, and the artifact includes bundled runtime history.

Mitigation: Sanitize identifiers before filesystem use and clear bundled runtime history before installation or redistribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whhaijun/skills/smart-agent-template)
- [README](README.md)
- [Agent workflow standard](AGENTS.md)
- [WBS rules](process-standards/core/WBS_RULES_v3.0.md)
- [Task reporting standard](process-standards/core/TASK_REPORTING_v3.0.md)
- [Context management standard](process-standards/core/CONTEXT_MANAGEMENT_v2.0.md)
- [Security check standard](process-standards/core/SECURITY_CHECK.md)
- [Multi-agent collaboration](docs/MULTI_AGENT_COLLABORATION.md)
- [Feishu integration](integrations/feishu/README.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown documentation with shell command examples, configuration files, and optional Python and shell integration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow templates, process standards, memory templates, auto-update configuration, and optional messaging bot integration examples.]

## Skill Version(s):

1.1.0 (source: server release metadata and target metadata; README badge agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
