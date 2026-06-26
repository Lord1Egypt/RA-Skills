## Description: <br>
Safely uninstall and reinstall OpenClaw while preserving user configurations, credentials, memory files, skills, and custom settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Albertpan2018](https://clawhub.ai/user/Albertpan2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to perform a clean reinstall, back up and restore OpenClaw data, remove stale files or third-party modifications, and restart or health-check the OpenClaw gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reinstall procedure includes destructive cleanup commands that can remove OpenClaw state and related directories. <br>
Mitigation: Review each shell command before running it, make a verified backup first, and confirm the exact paths targeted by uninstall or rm -rf commands. <br>
Risk: The backup may contain sensitive credentials, gateway tokens, memory, identity files, and prior agent state. <br>
Mitigation: Store backups in a protected location, restrict permissions, and treat restored or copied data as secret-bearing material. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Albertpan2018/reinstall-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/Albertpan2018) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash command blocks and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes backup, uninstall, reinstall, restore, and troubleshooting steps; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
