## Description: <br>
Backup and restore OpenClaw workspace, configs, and agent data to a Synology NAS via SMB or SSH/rsync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure, run, verify, and restore OpenClaw backups on a Synology NAS. It supports manual backup operations, scheduled backups, health checks, and recovery from dated snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore can copy API-key secrets into a pre-restore snapshot on the NAS even when normal backup docs describe .env as opt-in. <br>
Mitigation: Before restore, edit the script or restrict the NAS share so pre-restore snapshots cannot expose API keys; keep NAS storage encrypted or tightly access-controlled. <br>
Risk: Backups may include sensitive OpenClaw workspace, config, cron, and agent data. <br>
Mitigation: Use a dedicated non-admin NAS account with access only to the backup share, test with --dry-run, and review backupPaths before scheduling automated runs. <br>
Risk: Remote backup transport depends on NAS network and authentication configuration. <br>
Mitigation: Use Tailscale or a VPN for remote access, avoid exposing SMB publicly, pre-provision SSH host keys, and use SSH key authentication for SSH transport. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pfrederiksen/synology-backup) <br>
- [Publisher profile](https://clawhub.ai/user/pfrederiksen) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Tailscale](https://tailscale.com) <br>
- [Tailscale downloads](https://tailscale.com/download) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rsync and jq; SMB mode also requires cifs-utils and a chmod 600 credentials file.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
