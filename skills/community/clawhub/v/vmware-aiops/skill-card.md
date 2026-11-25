## Description:

Manages VMware vSphere and ESXi virtual machine lifecycle, deployments, guest operations, clusters, alarms, and infrastructure investigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

VMware administrators and infrastructure engineers use the skill to inspect VMware environments and manage VM lifecycle, deployments, clusters, alarms, and guest operations through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad VMware changes, and some operations act on their first call.

Mitigation: Use a dedicated least-privilege vCenter or ESXi account and review the target and scope before state-changing operations.

Risk: Guest commands run with the supplied guest account and may affect the guest system.

Mitigation: Use a least-privilege guest account and review each command and its target before execution.

Risk: When configured, webhooks can send issue and alarm details that may contain infrastructure identifiers.

Mitigation: Keep webhooks disabled unless needed; use approved endpoints and check what infrastructure details they receive.

Risk: Setup changes, external model examples, or support-sharing guidance may expose configuration or environment details.

Mitigation: Review configuration changes before applying them, and remove secrets and sensitive infrastructure details before sharing or sending examples externally.

## Reference(s):

- [VMware AIops project homepage](https://github.com/vmware-skills/VMware-AIops)
- [Capabilities and operation boundaries](artifact/references/capabilities.md)
- [Setup guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Investigation protocol](artifact/references/investigation-protocol.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Configuration instructions]

**Output Format:** [Natural-language guidance and structured VMware tool calls or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate state-changing VMware operations and guest commands when requested.]

## Skill Version(s):

2.5.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
