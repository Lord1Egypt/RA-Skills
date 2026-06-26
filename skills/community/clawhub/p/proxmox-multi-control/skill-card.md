## Description: <br>
Manage one or many Proxmox VE servers via REST API, including cluster-wide overview commands, node, VM, and container listing, power actions, snapshots, backups, storage, and task inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maikimolto](https://clawhub.ai/user/maikimolto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to let an agent inspect and administer one or more Proxmox VE hosts. It supports read-only status checks and higher-impact operations such as power control, snapshots, rollback, backups, storage, and task history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Proxmox hosts and perform high-impact infrastructure actions such as power operations, snapshot deletion, and rollback. <br>
Mitigation: Require explicit user confirmation before power actions, snapshot deletion, or rollback, and use a dedicated Proxmox account with the minimum required permissions. <br>
Risk: Credentials, token IDs, hostnames, VM names, backups, and task history may expose sensitive infrastructure information. <br>
Mitigation: Store credentials in a locked-down credentials file, avoid broad or root tokens, and treat command outputs as sensitive. <br>
Risk: Disabling TLS verification for self-signed certificates can reduce connection assurance. <br>
Mitigation: Enable TLS verification where practical and limit unverified connections to trusted networks. <br>


## Reference(s): <br>
- [Proxmox Multi Control on ClawHub](https://clawhub.ai/maikimolto/proxmox-multi-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON with ok/data fields; multi-host results include _host tags.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
