## Description: <br>
Cross-platform auto-start service manager for Windows and macOS. Supports installing, uninstalling, starting, stopping, and monitoring services with automatic restart. Use when you need to set up persistent background services that survive system reboots on Windows (sc/schtasks) or macOS (launchd). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahao2001](https://clawhub.ai/user/ahao2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure persistent background services for Windows or macOS systems, including install, uninstall, start, stop, status, logging, health monitoring, and restart behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent autostart configuration can create high-impact system changes, including Windows tasks that may run as SYSTEM and macOS launchd entries. <br>
Mitigation: Review the JSON configuration before installation and confirm every program path, argument, and working directory is trusted. <br>
Risk: The artifact includes an unrelated publisher upload script with a hardcoded API key. <br>
Mitigation: Do not run publish_textonly.py; the publisher should remove it from the distributed skill and revoke the embedded API key. <br>
Risk: Install and uninstall scripts require elevated privileges and can modify system startup behavior. <br>
Mitigation: Run install or uninstall commands only in a controlled environment after reviewing the target service name and startup configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahao2001/universal-autostart) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for service setup and configuration; generated commands may make persistent system changes when executed by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
