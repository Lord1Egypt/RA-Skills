## Description:

Enforces Revenium budget guardrails for OpenClaw agents, warning or halting work when configured limits are reached and metering usage into Revenium.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johndemic](https://clawhub.ai/user/johndemic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw agents to Revenium for spend metering, budget warnings, and optional halt-on-breach enforcement across normal agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content and usage metadata may be sent to Revenium as part of metering.

Mitigation: Install only where this telemetry is acceptable, and review credential and data handling before use on sensitive workspaces.

Risk: Persistent guardrail checks and cron jobs can affect all agent work, including warning or halting operations.

Mitigation: Review configured budget rules and halt mode, and document uninstall and clear-halt steps before deployment.

Risk: Installation can change agent sandbox, plugin, approval, and credential-injection configuration.

Mitigation: Apply in a controlled workspace, scope credentials, and plan rollback for plugin, exec-approval, sandbox, and cron changes.

## Reference(s):

- [Revenium AI Agents Documentation](https://docs.revenium.io/for-ai-agents)
- [Revenium Budget Enforcement on ClawHub](https://clawhub.ai/johndemic/skills/revenium)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Revenium CLI Repository](https://github.com/revenium/revenium-cli)
- [NemoClaw/OpenShell Setup](docs/nemoclaw-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit budget warnings, permission prompts, halt messages, setup commands, and status summaries.]

## Skill Version(s):

0.6.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
