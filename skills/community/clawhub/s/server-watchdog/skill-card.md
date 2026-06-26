## Description: <br>
Monitor remote servers over SSH, check service, database, disk, and memory health, restart crashed services when configured, and send alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Qoohsuan](https://clawhub.ai/user/Qoohsuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect server health, diagnose service or database failures, and apply monitored restart procedures for PM2, systemd, Docker, and MongoDB environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact control over remote services and automatic restarts. <br>
Mitigation: Use it only on servers where automatic MongoDB restarts are explicitly acceptable, and require human approval before production restarts. <br>
Risk: Environment-specific hostnames, paths, chat IDs, and alert text may be unsuitable or sensitive if reused unchanged. <br>
Mitigation: Edit all hostnames, file paths, chat IDs, and alert text before deployment. <br>
Risk: Password-based SSH examples weaken host verification when used unchanged. <br>
Mitigation: Prefer SSH keys with verified host keys. <br>
Risk: The persistent watchdog depends on install-time Node.js packages. <br>
Mitigation: Review and pin dependencies before installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Qoohsuan/server-watchdog) <br>
- [Qoohsuan publisher profile](https://clawhub.ai/user/Qoohsuan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational guidance for SSH checks, service restarts, watchdog deployment, and alert summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
