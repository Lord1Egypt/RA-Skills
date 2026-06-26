## Description: <br>
Manages VMware storage tasks including datastore browsing, deployable image discovery, iSCSI target configuration, and vSAN health and capacity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect VMware datastores, configure iSCSI storage, and check vSAN health and capacity from CLI or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change VMware storage configuration, including iSCSI adapter and target settings. <br>
Mitigation: Use least-privilege vCenter or ESXi accounts, run dry-run first, require explicit review for write actions, and verify hosts, targets, and LUN usage before applying changes. <br>
Risk: The skill requires local VMware connection configuration and per-target credentials. <br>
Mitigation: Prefer a secret manager over stored .env passwords, keep credential files at owner-only permissions, and enable certificate validation where possible. <br>
Risk: The security scan reports a suspicious verdict because package/source evidence does not clearly match the skill's safety claims. <br>
Mitigation: Verify the package version and source before installing, review the skill and scan results before deployment, and install only in environments where VMware storage administration access is acceptable. <br>


## Reference(s): <br>
- [VMware Storage source repository](https://github.com/zw008/VMware-Storage) <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-storage) <br>
- [Capabilities reference](references/capabilities.md) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Setup guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown with inline shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CLI or MCP guidance for vSphere storage operations; write operations should use dry-run and explicit confirmation.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
