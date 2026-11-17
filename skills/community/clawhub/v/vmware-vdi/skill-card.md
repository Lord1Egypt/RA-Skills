## Description:

Operates VMware and Omnissa Horizon VDI environments by inspecting and managing desktop pools, farms, sessions, machines, entitlements, health, and instant-clone images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

VDI administrators and help-desk teams use this skill to monitor Horizon health and manage desktop pools, sessions, machines, entitlements, and image rollouts through a Connection Server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TLS troubleshooting guidance includes disabling certificate checks, which could expose credentials or sensitive session data to interception.

Mitigation: Keep TLS verification enabled. Use disabled verification only for self-signed lab certificates where credential and session data are not at risk.

Risk: The security scan is incomplete because two local references were unresolved.

Mitigation: Resolve and review the missing references before relying on the scan assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/vmware-vdi)
- [Source repository (listed in skill documentation)](https://github.com/vmware-skills/VMware-VDI)
- [Capabilities reference](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup guide](artifact/references/setup-guide.md)
- [VMware AIOps companion skill](https://github.com/vmware-skills/VMware-AIops)
- [VMware Monitor companion skill](https://github.com/vmware-skills/VMware-Monitor)
- [VMware NSX Security companion skill](https://github.com/vmware-skills/VMware-NSX-Security)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text and structured MCP responses with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read results, operational previews, or confirmed Horizon actions.]

## Skill Version(s):

2.4.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
