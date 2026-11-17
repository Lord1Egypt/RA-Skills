## Description:

Provides a Chinese-language workflow for safely modifying OpenClaw configuration with confirmation, validation, repair, backup comparison, and gateway status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoxia](https://clawhub.ai/user/nicoxia)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to plan, confirm, apply, repair, and verify OpenClaw configuration changes. It is especially focused on gateway, channel, model, session, and authentication settings in ~/.openclaw/openclaw.json.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks the agent to record repair lessons into persistent memory, which may capture tokens, authentication settings, endpoints, host-specific values, or raw diffs if used without review.

Mitigation: Require explicit user confirmation before any MEMORY.md update, redact sensitive and host-specific values, and save only scoped configuration lessons that have been reviewed for accuracy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nicoxia/skills/safe-config-workflow-zh-cn)
- [OpenClaw Configuration Documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration)
- [OpenClaw Doctor Documentation](https://docs.openclaw.ai/zh-CN/cli/doctor)
- [OpenClaw Gateway Manual](https://docs.openclaw.ai/zh-CN/gateway/index.md)
- [OpenClaw Gateway Troubleshooting](https://docs.openclaw.ai/zh-CN/gateway/troubleshooting)
- [OpenClaw FAQ](https://docs.openclaw.ai/zh-CN/help/faq.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmation prompts, filtered diagnostic summaries, backup diff explanations, and gateway verification results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
