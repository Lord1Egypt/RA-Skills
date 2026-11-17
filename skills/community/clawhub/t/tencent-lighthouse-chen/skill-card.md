## Description:

Manage Tencent Cloud Lighthouse instances through mcporter and a Lighthouse MCP server, including instance queries, monitoring and alerting, firewall rules, snapshots, diagnostics, and remote commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure an agent for Tencent Cloud Lighthouse administration, inspect instances, review monitoring data, manage firewall settings, and run approved remote commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tencent Cloud API keys are written into the mcporter configuration file in plaintext.

Mitigation: Use a dedicated least-privilege CAM identity, restrict permissions on ~/.mcporter/mcporter.json, and rotate credentials after testing or suspected exposure.

Risk: Setup and execution rely on npm or npx packages that are not pinned in the artifact.

Mitigation: Review or pin the mcporter and Lighthouse MCP server packages before installation, especially before granting credentials.

Risk: The skill can guide firewall changes and remote command execution against cloud instances.

Mitigation: Confirm the target Region, InstanceId, and command intent before running state-changing or remote-execution operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jason-aka-chen/skills/tencent-lighthouse-chen)
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses commonly include mcporter commands, setup checks, Tencent Cloud region and instance identifiers, and structured JSON output guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
