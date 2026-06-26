## Description: <br>
System resource monitoring (CPU, memory, disk, network). Use when user asks "system status", "CPU usage", "memory usage", "disk space", or wants to monitor system resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yushimohuang](https://clawhub.ai/user/yushimohuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and users can ask an agent to inspect local CPU, memory, disk, network, uptime, process, and temperature information when troubleshooting or checking machine health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local diagnostic output can reveal private system details such as process command lines, IP addresses, folder names, disk usage, and project paths. <br>
Mitigation: Review and redact process, disk, and network output before sharing it outside the local environment. <br>
Risk: Watch mode continuously runs foreground monitoring and repeatedly refreshes terminal output. <br>
Mitigation: Use watch mode only when continuous monitoring is intended, and stop it when the diagnostic session is complete. <br>


## Reference(s): <br>
- [System Monitor README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/yushimohuang/system-monitor-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style terminal output with local system resource summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local diagnostic shell commands; watch mode can refresh continuously until stopped.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
