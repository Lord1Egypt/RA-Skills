## Description: <br>
Reports local disk usage, uptime, and operating system information using standard read-only system commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aneasystone](https://clawhub.ai/user/aneasystone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to ask an agent for a quick local machine status summary, including filesystem usage, kernel or operating system details, and uptime/load information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command output can reveal local system, load, kernel, and mount information. <br>
Mitigation: Use only when the user is comfortable sharing local machine status with the agent, and review the displayed df, uname, and uptime output before redistributing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aneasystone/sysinfo-demo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Plain text command output followed by a brief summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses df -h, uname -a, and uptime on Darwin or Linux; does not require sudo or write access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
