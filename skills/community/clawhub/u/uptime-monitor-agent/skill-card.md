## Description: <br>
Monitor uptime of websites/services and alert when down. Use when checking if a website is reachable, monitoring service health, or getting alerted on downtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check whether configured HTTP endpoints are reachable, alert on downtime, and summarize recent uptime from local logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts user-specified URLs and writes status details to local logs. <br>
Mitigation: Monitor only approved endpoints and avoid placing secrets or sensitive tokens in monitored URLs. <br>
Risk: Webhook or email alerts can disclose service names, URLs, status codes, timing, and outage details to configured destinations. <br>
Mitigation: Send alerts only to destinations approved to receive operational status information. <br>
Risk: The skill runs local shell scripts that use curl against configured targets. <br>
Mitigation: Review the scripts and environment variables before running them in a production environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kryzl19/uptime-monitor-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, pipe-delimited status output, and Markdown uptime reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and uses user-provided endpoint, alert, and interval configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
