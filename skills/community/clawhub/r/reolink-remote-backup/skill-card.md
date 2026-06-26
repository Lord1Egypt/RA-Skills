## Description: <br>
Set up reliable off-site Reolink camera backup when cameras are remote (4G/5G/LTE) and home inbound networking is constrained (CGNAT/locked routers). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccaprani](https://clawhub.ai/user/ccaprani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, systems administrators, and technical home users use this skill to plan and configure off-site Reolink camera backup through a VPS relay when direct camera-to-home ingestion is impractical. It provides setup guidance for FTP/FTPS ingest, local or NAS pull sync, retention, health checks, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run privileged setup scripts that reconfigure a VPS, install network services, and open firewall ports. <br>
Mitigation: Review each script before running it, use a dedicated VPS, and restrict firewall access where practical. <br>
Risk: FTP/FTPS ingest and remote sync can expose camera backups or credentials if configured loosely. <br>
Mitigation: Keep FTPS enabled except for tightly controlled debugging, isolate the FTP ingest user from admin users, use SSH keys for administration, and rotate credentials exposed in chat or logs. <br>
Risk: Ongoing systemd and cron jobs can sync or delete files after initial setup. <br>
Mitigation: Use a numeric retention window, keep the default /srv/reolink path unless path validation is added, verify destination paths before enabling sync, and know how to disable the systemd timer and remove the cron retention job. <br>


## Reference(s): <br>
- [Reolink Remote Backup Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ccaprani/reolink-remote-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and bundled bash setup scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides privileged VPS setup, local systemd user timer setup, and cron-based retention for a Reolink backup relay.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
