## Description: <br>
Manages SSH-accessible Linux/Unix servers through connection checks, remote command execution, file transfer, monitoring, service management, log review, and security checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickliang](https://clawhub.ai/user/nickliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to administer configured Linux/Unix servers over SSH, including command execution, file transfer, monitoring, service management, log inspection, and security checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad remote administrative power over SSH-accessible servers. <br>
Mitigation: Install only for intended server administration, use least-privilege SSH accounts, prefer keys over passwords, and avoid production or root credentials where possible. <br>
Risk: Remote commands, file transfers, log cleanup, hardening, recursive transfer, and preset upload functions can make destructive or hard-to-recover changes. <br>
Mitigation: Review exact commands and paths before execution, keep backups, and use the highest-risk operations only when a recovery path is available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nickliang/ssh-remote-sanitized) <br>
- [README.md](artifact/README.md) <br>
- [Quick configuration guide](artifact/docs/快速配置指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style operational responses with command output summaries and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote command output, file transfer status, system metrics, service status, log excerpts, and security recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
