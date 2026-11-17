## Description:

Provides a Chinese workflow for safely modifying OpenClaw configuration by requiring documentation checks, user confirmation, doctor --fix validation, backup diffs, gateway status checks, and concise feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoxia](https://clawhub.ai/user/nicoxia)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators maintaining OpenClaw Gateway use this skill to plan, confirm, apply, validate, and explain configuration changes. It is intended for configuration workflows where the agent should check documentation, preserve backups, summarize repairs, and verify service health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can persist learned configuration details into MEMORY.md, which may capture sensitive configuration values if entries are not reviewed and redacted.

Mitigation: Require explicit review before writing MEMORY.md entries and redact raw tokens, authentication values, session identifiers, endpoints, logs, and unredacted configuration diffs.

Risk: The workflow can change OpenClaw Gateway configuration and run doctor --fix, which may alter runtime behavior or overwrite configuration values.

Mitigation: Confirm the requested change and impact with the user, preserve backups, inspect diffs after repair, and verify gateway status before considering the change complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicoxia/skills/safe-config-workflow)
- [OpenClaw configuration documentation](https://docs.openclaw.ai/zh-CN/gateway/configuration)
- [OpenClaw doctor documentation](https://docs.openclaw.ai/zh-CN/cli/doctor)
- [OpenClaw Gateway manual](https://docs.openclaw.ai/zh-CN/gateway/index.md)
- [OpenClaw Gateway troubleshooting](https://docs.openclaw.ai/zh-CN/gateway/troubleshooting)
- [OpenClaw FAQ](https://docs.openclaw.ai/zh-CN/help/faq.md)
- [Artifact test guide](artifact/TEST-GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include configuration-change confirmations, filtered doctor output, backup diff summaries, gateway status results, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
