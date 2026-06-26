## Description: <br>
SysGuard provides OpenClaw system monitoring, health checks, diagnostics, text trend charts, cache cleanup, notifications, and continuous gateway monitoring from shell-based commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steventsang18](https://clawhub.ai/user/steventsang18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators and operators use this skill in trusted operations channels to inspect host and gateway health, generate diagnostic reports, view recent trends, clean caches, and receive alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Host diagnostics and cleanup commands can be triggered through chat-based use. <br>
Mitigation: Install only where the OpenClaw bot is limited to trusted administrators or private operations channels. <br>
Risk: The cleanup command can remove temporary files, package cache data, journal logs, and old history records. <br>
Mitigation: Review or disable cleanup behavior before deployment and document what data retention policy it enforces. <br>
Risk: Alert notifications may leave the host through Feishu or WeCom webhook URLs. <br>
Mitigation: Store webhook URLs as secrets, restrict channel membership, and document the external notification destination. <br>
Risk: Continuous monitoring can run as a long-lived process. <br>
Mitigation: Document how to start, supervise, and stop the monitor process before enabling it. <br>


## Reference(s): <br>
- [SysGuard ClawHub listing](https://clawhub.ai/steventsang18/sysguard) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [IM-friendly plain text and Markdown status panels, diagnostic reports, trend charts, alert messages, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute host diagnostics, cache cleanup, outbound webhook notifications, and continuous monitoring loops.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
