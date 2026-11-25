## Description:

Operates VMware/Omnissa Horizon VDI environments through the Connection Server to monitor and manage pools, farms, sessions, desktops, entitlements, events, health, and instant-clone images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

VDI administrators and help-desk operators use this skill to inspect Horizon health, pools, sessions, and entitlements, and to manage desktops or publish images with a preview of the affected users and resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some write actions can disrupt users, and pushing an image recreates every desktop in the pool.

Mitigation: Review the write preview and blast radius, then confirm only after the affected users and resources are understood.

Risk: After a write timeout or gateway error, the change may already have completed; retrying immediately can repeat the action.

Mitigation: Inspect the Horizon target state before retrying a write.

Risk: The scanner rated the release benign with medium confidence but marked analysis partial because two local references could not be resolved.

Mitigation: Review the setup option and the unresolved references if they affect your use.

Risk: The setup guide says the locally stored password is obfuscated rather than encrypted.

Mitigation: Inject the password from a secret manager when stronger credential protection is needed.

## Reference(s):

- [Setup Guide](artifact/references/setup-guide.md)
- [Capabilities](artifact/references/capabilities.md)
- [CLI Reference](artifact/references/cli-reference.md)
- [MCP Result Contract](artifact/references/mcp-result-contract.md)
- [Project repository (listed in the skill documentation)](https://github.com/vmware-skills/VMware-VDI)
- [PyPI package](https://pypi.org/project/vmware-vdi/)

## Skill Output:

**Output Type(s):** [Text, JSON, Operational guidance, Shell commands, Configuration instructions]

**Output Format:** [Natural-language guidance and structured Horizon results from CLI or MCP calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status data, write previews, and blast-radius details; write actions use confirmation gates.]

## Skill Version(s):

2.4.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
