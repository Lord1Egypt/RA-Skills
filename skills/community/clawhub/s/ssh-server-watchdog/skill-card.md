## Description: <br>
Monitor remote servers via SSH to check service health, database status, disk space, and memory, and to restart crashed services with messaging alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qoohsuan](https://clawhub.ai/user/qoohsuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to diagnose remote server health over SSH, inspect PM2, systemd, Docker, and database status, and prepare restart or watchdog deployment steps for services that are down. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide or deploy automated restarts for remote services, which may interrupt production workloads if used without approval. <br>
Mitigation: Require manual approval before restarts or PM2 watchdog deployment unless unattended auto-healing is explicitly intended for the target server. <br>
Risk: The SSH examples and watchdog defaults include unsafe or host-specific settings such as disabled host key checking, administrator references, and a hard-coded Telegram chat ID. <br>
Mitigation: Review and replace all defaults before use, remove the hard-coded chat ID and host-specific references, configure the alert recipient explicitly, and prefer SSH keys with host verification enabled. <br>


## Reference(s): <br>
- [SSH Server Watchdog on ClawHub](https://clawhub.ai/qoohsuan/ssh-server-watchdog) <br>
- [Publisher profile: qoohsuan](https://clawhub.ai/user/qoohsuan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration notes, and optional JavaScript watchdog code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational recommendations for service restarts, monitoring setup, and alert configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
