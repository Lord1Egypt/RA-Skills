## Description:

Provides read-only VMware/vSphere/ESXi inventory, health, alarm, event, and VM/host/datastore investigations, including cross-cluster and cross-vCenter triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

VMware administrators and infrastructure engineers use this skill to inspect vCenter and ESXi inventory, health, alarms, events, and performance, and to triage issues across clusters and vCenters. It provides read-only infrastructure investigation; changes require a separately routed skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review evidence is partial, and setup references an unpinned `npx skills` installer.

Mitigation: Review the installer source and setup instructions, and use a known pinned version where possible before installation.

Risk: If the optional daemon webhooks are enabled, they send issue counts and warning details to configured URLs; payloads can include entity names and sanitized, truncated alarm, event, or log text, and connection errors may include host names, IPs, or user names.

Mitigation: Keep webhooks disabled unless needed, configure only a trusted endpoint, and review the disclosed operational data before enabling them.

Risk: The skill requires credentials for configured vCenter or ESXi targets.

Mitigation: Follow the setup guidance for local credential handling and use a dedicated vCenter account with the Read-Only role.

## Reference(s):

- [VMware Monitor project](https://github.com/vmware-skills/VMware-Monitor)
- [Model fit self-test guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md)
- [Capabilities](artifact/references/capabilities.md)
- [Setup guide](artifact/references/setup-guide.md)
- [Investigation protocol](artifact/references/investigation-protocol.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Operational guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown summaries and VMware query guidance, with CLI or MCP calls as appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only infrastructure findings; local configuration and audit guidance]

## Skill Version(s):

2.6.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
