## Description: <br>
Use this skill when an agent needs to manage VMware vSphere storage, including datastores, iSCSI targets, and vSAN health and capacity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and infrastructure operators use this skill to inspect datastores, find deployable images, manage iSCSI host targets, and check vSAN health and capacity through CLI or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer VMware storage and uses credentials for vCenter or ESXi targets. <br>
Mitigation: Install only for agents that should manage VMware storage, use a least-privileged vSphere account, and protect the per-target password environment variables. <br>
Risk: TLS verification and authentication bypass guidance can weaken production safeguards if used casually. <br>
Mitigation: Set certificate verification to true in production and reserve --skip-auth for isolated diagnostics. <br>
Risk: iSCSI target changes and storage rescans can affect host storage state during sensitive windows. <br>
Mitigation: Require explicit human approval, prefer dry-run previews, and schedule changes during approved maintenance windows. <br>
Risk: Notification or webhook configuration could expose operational storage details. <br>
Mitigation: Review webhook destinations and payload handling before enabling notifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-storage) <br>
- [Project homepage](https://github.com/zw008/VMware-Storage) <br>
- [VMware Storage Capabilities](references/capabilities.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [VMware Policy auto-remediation pattern docs](https://github.com/zw008/VMware-Policy/blob/main/docs/auto-remediation-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured CLI or MCP guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-shaped CLI or MCP output examples when describing storage results.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
