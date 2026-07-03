## Description: <br>
Use this skill to manage VMware NSX security operations including distributed firewall policies and rules, security groups, VM tags, Traceflow diagnostics, and IDPS status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security operators use this skill to inspect and change NSX distributed firewall policy, security groups, VM tags, Traceflow diagnostics, and IDS/IPS settings through CLI or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change NSX firewall and security policy. <br>
Mitigation: Use it only from agent profiles intended for NSX administration, require explicit approval for write operations, use dry-run previews where available, and review audit logs. <br>
Risk: NSX credentials are required for configured targets. <br>
Mitigation: Use a dedicated scoped NSX account, inject production passwords from a secret manager, and keep config and .env files owner-only. <br>
Risk: Incorrect DFW rules or tag-based groups can disrupt access or leave workloads unprotected. <br>
Mitigation: Verify tag inventory, preserve management allow rules before default-deny changes, and use Traceflow before and after policy changes. <br>
Risk: The release is third-party software that may be used against production firewall policy. <br>
Mitigation: Review the PyPI/GitHub package and source history before production deployment. <br>


## Reference(s): <br>
- [VMware NSX Security project homepage](https://github.com/zw008/VMware-NSX-Security) <br>
- [Capabilities reference](references/capabilities.md) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Setup guide](references/setup-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-nsx-security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local CLI or MCP tool use against configured NSX Manager targets.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
