## Description: <br>
VPS server maintenance and optimization guidance for initial setup, security hardening, performance tuning, time synchronization, and routine maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaowenzhou](https://clawhub.ai/user/xiaowenzhou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and system administrators use this skill to generate VPS setup, hardening, performance tuning, cleanup, and operational maintenance guidance for Debian or Ubuntu-style servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Root-level server administration commands can lock users out of a VPS when SSH, firewall, timezone, NTP, or access settings are copied without adaptation. <br>
Mitigation: Review each command before use, keep provider console or another recovery path available, test SSH access before enabling restrictive firewall rules, and adapt ports and service settings to the target host. <br>
Risk: Broad cleanup commands can delete system data or logs if used as-is on production systems. <br>
Mitigation: Replace broad deletion commands with dry-run, age-based, or path-scoped cleanup steps before running them on production servers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaowenzhou/vps-maintenance) <br>
- [Publisher profile](https://clawhub.ai/user/xiaowenzhou) <br>
- [Debian package mirror](https://deb.debian.org/debian/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks, command tables, and checklist items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contains root-level server administration commands that should be reviewed and adapted before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
