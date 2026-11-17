## Description:

Safe Config Workflow guides agents through safe OpenClaw configuration changes with documentation checks, user confirmation, validation, repair, backup comparison, and gateway status verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoxia](https://clawhub.ai/user/nicoxia)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to modify OpenClaw Gateway, channel, model, session, and authentication configuration with a repeatable review and validation workflow. It is intended for agents that need to inspect documentation, request confirmation, run OpenClaw diagnostics, summarize repairs, and verify gateway health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration files and logs may contain tokens, credentials, private endpoints, or account details.

Mitigation: Review diagnostic summaries before sharing them and redact sensitive values from configuration diffs, logs, and user-facing output.

Risk: The workflow can persist learned configuration details to memory.

Mitigation: Show proposed MEMORY.md entries before writing them and require explicit user consent for persistent memory updates.

Risk: Automatic repair commands may change OpenClaw configuration in ways that affect Gateway behavior.

Mitigation: Confirm the requested change with the user, compare backups after repair, and verify Gateway status after the change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nicoxia/skills/safe-config-workflow-zh)
- [OpenClaw Configuration Documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration)
- [OpenClaw Doctor Documentation](https://docs.openclaw.ai/zh-CN/cli/doctor)
- [OpenClaw Gateway Manual](https://docs.openclaw.ai/zh-CN/gateway/index.md)
- [OpenClaw Gateway Troubleshooting](https://docs.openclaw.ai/zh-CN/gateway/troubleshooting)
- [OpenClaw FAQ](https://docs.openclaw.ai/zh-CN/help/faq.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes relevant diagnostic output and configuration changes for the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
