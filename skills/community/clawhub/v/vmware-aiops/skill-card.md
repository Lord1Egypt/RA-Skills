## Description:

Manage VMware vSphere and ESXi VM lifecycles, deployments, guest operations, clusters, alarms, datastore images, and read-only infrastructure investigations through agent tools and CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to inspect VMware environments and manage VM, cluster, deployment, guest-operation, and alarm workflows. It can make changes in connected environments, so its permissions depend on the configured vCenter/ESXi and guest accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence and notes that some referenced material was not fully inspected.

Mitigation: Before installing, review project-rule changes, the exposed MCP service and write permissions, guest command limits, and any requests to share diagnostics.

Risk: The skill can change VMware state, and some create, clone, deploy, power-on, and reconfigure operations act on their first call; access follows the connected account's permissions.

Mitigation: Use a dedicated least-privilege vCenter/ESXi account, review operation parameters and any available blast-radius preview, and approve state changes deliberately.

Risk: Guest commands run with the supplied guest account, and guest file upload can read files available to the server process.

Mitigation: Use a least-privilege guest account and restrict which local files the server process can access; review commands and transfer paths before execution.

Risk: When configured, diagnostic webhooks can share alarm, event, and host-log details, including entity names and potentially host, IP, or user identifiers.

Mitigation: Keep webhooks disabled unless needed, use destinations you control, and review the diagnostic data sent before enabling them.

## Reference(s):

- [Setup and security guide](references/setup-guide.md)
- [Tool capabilities and limits](references/capabilities.md)
- [Agent guardrails](references/agent-guardrails.md)
- [CLI reference](references/cli-reference.md)
- [Investigation protocol](references/investigation-protocol.md)
- [Project homepage (skill metadata)](https://github.com/vmware-skills/VMware-AIops)
- [ClawHub release page](https://clawhub.ai/zw008/skills/vmware-aiops)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Files]

**Output Format:** [Structured tool calls and text summaries, with CLI commands and configuration guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate read or write operations against connected VMware targets; available actions and results depend on configured permissions and environment.]

## Skill Version(s):

2.5.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
