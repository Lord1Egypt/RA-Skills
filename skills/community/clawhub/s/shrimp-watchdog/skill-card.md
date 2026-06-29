## Description: <br>
Keep OpenClaw gateway alive with heartbeat monitoring, auto-restart, crash alerts, memory warnings, and uptime reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarrymo](https://clawhub.ai/user/sarrymo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to monitor an OpenClaw Gateway process, restart it when health checks fail, receive crash or recovery alerts, and review uptime reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires root/systemd control to monitor and restart openclaw-gateway. <br>
Mitigation: Install it only on systems where granting root/systemd control is acceptable, and review proposed systemctl actions before deployment. <br>
Risk: Automatic gateway restarts can interrupt active OpenClaw Gateway sessions. <br>
Mitigation: Confirm the monitored port, heartbeat interval, stop/status workflow, and restart behavior before leaving the watchdog running. <br>


## Reference(s): <br>
- [OpenClaw Watchdog on ClawHub](https://clawhub.ai/sarrymo/shrimp-watchdog) <br>
- [Publisher profile: sarrymo](https://clawhub.ai/user/sarrymo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and status or alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose root/systemd operations and configurable monitoring parameters such as port, interval, and memory threshold.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
