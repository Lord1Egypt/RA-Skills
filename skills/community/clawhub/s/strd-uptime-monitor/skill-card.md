## Description: <br>
Monitor uptime of websites/services and alert when down. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check HTTP endpoint reachability, send outage alerts through configured webhook or email channels, and generate Markdown uptime reports from local logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes HTTP requests to user-provided URLs. <br>
Mitigation: Monitor only endpoints you are authorized to check and avoid embedding secrets in monitored URLs. <br>
Risk: Configured webhook or email alerts can send outage details outside the local environment. <br>
Mitigation: Use a narrowly scoped alert destination and review what endpoint details are included before enabling alerts. <br>
Risk: Local status and alert logs may contain endpoint names or outage history. <br>
Mitigation: Periodically clear or protect local uptime logs when endpoint names or history are sensitive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Status lines, webhook or email alert text, and Markdown uptime reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured URLs and optional webhook or email settings; writes local status and alert logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
