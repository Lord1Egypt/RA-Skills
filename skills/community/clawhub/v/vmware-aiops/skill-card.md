## Description: <br>
Manages VMware vSphere and ESXi VM lifecycle operations, including power, clone, snapshot, migration, deployment, guest execution, cluster changes, and vCenter alarm handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to administer VMware vSphere and ESXi VM lifecycle tasks, deployment workflows, guest operations, and alarm remediation with explicit checks and approval gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer VMware infrastructure and perform write operations that affect VMs, clusters, snapshots, migrations, and alarms. <br>
Mitigation: Install only for intended VMware administration, use a least-privilege vCenter account, require explicit approval for remediation, and prefer read-only companion skills for investigation first. <br>
Risk: Local VMware credentials and optional webhook URLs are sensitive configuration. <br>
Mitigation: Protect ~/.vmware-aiops/.env, keep file permissions restrictive, avoid storing real secrets in plain local files when a secret manager is available, and keep webhooks disabled unless needed. <br>
Risk: Guest execution and destructive lifecycle operations can disrupt running workloads. <br>
Mitigation: Use explicit parameters, dry-run support, double confirmation for destructive CLI actions, and audit logs before applying changes. <br>
Risk: TLS certificate validation bypass can weaken connection security. <br>
Mitigation: Leave SSL validation enabled for production and use bypass only for isolated lab environments with self-signed certificates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/vmware-aiops) <br>
- [Project homepage](https://github.com/zw008/VMware-AIops) <br>
- [Capabilities reference](references/capabilities.md) <br>
- [CLI reference](references/cli-reference.md) <br>
- [Investigation protocol](references/investigation-protocol.md) <br>
- [Setup guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, MCP tool-selection guidance, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include YAML or JSON configuration examples and shell commands for vmware-aiops.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
