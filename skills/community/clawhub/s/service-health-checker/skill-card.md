## Description: <br>
Monitor uptime of websites/services and alert when down. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to check HTTP endpoint reachability, log uptime status, send downtime alerts, and generate uptime summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring endpoints without authorization can violate policy or create unwanted traffic. <br>
Mitigation: Use the skill only for services the operator is authorized to monitor. <br>
Risk: URLs, internal hostnames, outage details, and alert destinations may be sensitive in logs or notifications. <br>
Mitigation: Use approved webhook or email destinations and protect or clear local logs when they contain sensitive service details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kryzl19/service-health-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain text status lines and Markdown uptime reports with shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local status and alert logs and may send webhook or email alerts when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
