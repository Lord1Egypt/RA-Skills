## Description: <br>
Operates TrueNAS SCALE storage through governed CLI and MCP workflows for health checks, ZFS pools, datasets, snapshots, disks, alerts, services, and replication tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and storage operators use this skill to triage and manage a TrueNAS SCALE appliance, inspect ZFS resources, and run guarded write actions such as scrubs, dataset creation, snapshots, and service restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a TrueNAS SCALE appliance and includes write actions such as snapshot deletion and service restart. <br>
Mitigation: Use a least-privilege TrueNAS API key, keep write operations under explicit human approval, and use dry-run or double-confirmation paths where available. <br>
Risk: Snapshot deletion is irreversible and service restarts can disrupt availability. <br>
Mitigation: Review the target resource before approval, create or verify a recovery snapshot when appropriate, and retain local audit logs for accountability. <br>
Risk: Credential handling includes an optional environment master password and legacy plaintext API-key migration path. <br>
Mitigation: Prefer the interactive prompt or a managed CI secret, migrate legacy plaintext keys promptly, and remove exported long-lived secrets after use. <br>
Risk: The release is preview and mock-validated, with TrueNAS endpoint paths still requiring live verification. <br>
Mitigation: Run diagnostics first and validate behavior against a non-production or low-risk appliance before routine operational use. <br>


## Reference(s): <br>
- [truenas-aiops capabilities](references/capabilities.md) <br>
- [truenas-aiops CLI reference](references/cli-reference.md) <br>
- [truenas-aiops setup and security guide](references/setup-guide.md) <br>
- [Project homepage from ClawHub metadata](https://github.com/AIops-tools/TrueNAS-AIops) <br>
- [ClawHub skill page](https://clawhub.ai/zw008/skills/truenas-aiops) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke CLI or MCP operations against a configured TrueNAS SCALE appliance; write actions should remain gated by human approval.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
