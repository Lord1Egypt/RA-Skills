## Description: <br>
Autonomous VPS monitoring and auto-remediation - kills runaway procs, frees disk, restarts dead services, hardens security. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[strouddustinn-bot](https://clawhub.ai/user/strouddustinn-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server administrators use this skill to monitor Linux VPS health and plan or run self-healing remediation for runaway processes, disk pressure, failed services, memory pressure, and security hardening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous remediation with root-level access can alter live processes, services, disk state, and firewall rules. <br>
Mitigation: Review the code, run dry-run first on a noncritical host, and enable cron or daemon mode only after thresholds and whitelists are tuned. <br>
Risk: The documented sudo curl install path is unpinned and may fetch changed code. <br>
Mitigation: Pin a trusted release or checksum and inspect the artifact before installing it with elevated privileges. <br>
Risk: Firewall and security actions may disrupt access despite approval-oriented safeguards. <br>
Mitigation: Keep security actions disabled until tested, require human approval for blocking changes, and maintain out-of-band recovery access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/strouddustinn-bot/vps-guardian) <br>
- [VPS Guardian documentation](https://vps-guardian.io/docs) <br>
- [VPS Guardian issue tracker](https://github.com/vps-guardian/guardian/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and INI configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for Linux VPS administration with root or sudo access; dry-run guidance is available before remediation.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
