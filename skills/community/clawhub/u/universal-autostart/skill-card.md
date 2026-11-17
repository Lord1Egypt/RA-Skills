## Description:

Cross-platform auto-start service manager for Windows and macOS. Supports installing, uninstalling, starting, stopping, and monitoring services with automatic restart. Use when you need to set up persistent background services that survive system reboots on Windows (sc/schtasks) or macOS (launchd).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahao2001](https://clawhub.ai/user/ahao2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure persistent background programs that start automatically after reboot on Windows or macOS. It provides guidance, commands, scripts, and JSON configuration patterns for installing, uninstalling, starting, stopping, monitoring, and restarting those services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent auto-start tasks that run with high privilege.

Mitigation: Install only for trusted programs, review the JSON configuration before use, and avoid SYSTEM or root defaults where a lower-privilege account is sufficient.

Risk: The package includes an unrelated publishing script with a hard-coded SkillHub upload credential.

Mitigation: Remove or review publish_textonly.py before deployment and rotate the exposed credential.

Risk: Uninstall behavior must target the same task or plist that was installed.

Mitigation: Verify the configured service name and confirm the exact scheduled task or launchd plist is removed during uninstall.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahao2001/skills/universal-autostart)
- [Publisher profile](https://clawhub.ai/user/ahao2001)
- [Project page listed in artifact documentation](https://gitee.com/steam2001/universal-autostart)
- [Issue tracker listed in artifact documentation](https://gitee.com/steam2001/universal-autostart/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include privileged install or uninstall commands and service configuration files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
