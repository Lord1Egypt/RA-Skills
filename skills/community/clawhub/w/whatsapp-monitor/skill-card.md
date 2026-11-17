## Description:

Real-time WhatsApp message monitor that tracks specified chats or groups for keyword hits and periodically aggregates matching messages to a Feishu (Lark) multi-dimensional table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhanson](https://clawhub.ai/user/mrhanson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor authorized WhatsApp chats or groups for configured keywords, collect matching messages, and export batches into Feishu multi-dimensional tables for review or alerting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can monitor private WhatsApp conversations and export matched content to Feishu.

Mitigation: Install and run it only for chats the operator is authorized to monitor, and align retention and export settings with the organization's privacy policy.

Risk: The OpenClaw WhatsApp gateway may expose chat APIs if bound beyond localhost or deployed without access controls.

Mitigation: Keep the gateway bound to localhost where possible, or protect any remote access with authenticated TLS and network restrictions.

Risk: Feishu credentials and table tokens are configured in JSON files and may be displayed by the wrapper's config command.

Mitigation: Store production secrets outside plaintext config when possible, restrict file permissions, and avoid running config-printing commands with real credentials.

Risk: Dependency ranges are not pinned to exact versions.

Mitigation: Pin and review dependencies before production deployment, then re-run tests and security scans after updates.

Risk: Setup and reset-style commands can modify local config, data, and logs.

Mitigation: Review setup and operational commands before running them on an existing deployment, and back up configuration and retained message data first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrhanson/skills/whatsapp-monitor)
- [OpenClaw WhatsApp integration guide](artifact/references/openclaw_whatsapp_integration.md)
- [OpenClaw Gateway port configuration](artifact/references/port_configuration.md)
- [OpenClaw integration guide](artifact/openclaw_integration.md)
- [Usage guide](artifact/USAGE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and generated local JSON/message-export data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monitors configured WhatsApp targets, writes matched messages to local JSON storage, and exports matching message records to Feishu when run with valid credentials.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
