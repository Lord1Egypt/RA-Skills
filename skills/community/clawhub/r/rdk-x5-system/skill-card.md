## Description: <br>
This skill helps manage RDK X5 system settings, backups and restores, OTA and miniboot upgrades, CPU/BPU frequency and thermal settings, kernel switching, systemd autostart, storage expansion, and basic system log or version checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and device operators use this skill to administer RDK X5 boards, including backups, upgrades, boot and kernel settings, service autostart, storage expansion, and system diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill proposes powerful RDK X5 device-management commands that can change firmware, boot behavior, services, storage, and system configuration. <br>
Mitigation: Install or use it only for managed RDK X5 devices, review every sudo command before approval, and keep a backup before upgrades or filesystem changes. <br>
Risk: Storage resizing, miniboot updates, and systemd autostart changes can make a device difficult to recover if applied to the wrong target or service. <br>
Mitigation: Verify device paths before resizing storage, avoid unsupported miniboot downgrades, and inspect each systemd ExecStart target before enabling a service. <br>


## Reference(s): <br>
- [Rdk X5 System on ClawHub](https://clawhub.ai/katherineedwards2475/rdk-x5-system) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require sudo and should be reviewed against the target RDK X5 device before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
