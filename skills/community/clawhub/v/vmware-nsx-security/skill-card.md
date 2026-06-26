## Description: <br>
Use this skill when an agent needs to manage VMware NSX security, including distributed firewall policies and rules, security groups, VM tags, Traceflow diagnostics, and IDS/IPS status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and security operators use this skill to inspect and manage VMware NSX distributed firewall policy, security groups, VM tags, Traceflow diagnostics, and IDS/IPS status through an agent-assisted CLI or MCP workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write operations can change firewall rules, security groups, VM tags, or IDS/IPS settings and affect production connectivity. <br>
Mitigation: Use a dedicated least-privilege NSX account, review dry-run output before writes, and require approval for changes. <br>
Risk: The skill requires NSX credentials and local configuration files. <br>
Mitigation: Protect the .env file, keep configuration permissions restricted, and avoid storing secrets in config.yaml. <br>
Risk: Agent-assisted NSX security guidance can be incorrect or incomplete for the target environment. <br>
Mitigation: Review proposed changes, validate with Traceflow or rule statistics where applicable, and rely on the built-in audit trail for accountability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-nsx-security) <br>
- [Project homepage](https://github.com/zw008/VMware-NSX-Security) <br>
- [Capabilities reference](references/capabilities.md) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Setup guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose read and write NSX security operations; write operations should be reviewed with dry-run output and audited execution.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
