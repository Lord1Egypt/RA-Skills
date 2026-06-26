## Description: <br>
Builds a website HTTP monitoring system that checks status codes and response latency on a schedule and generates daily HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yb0554](https://clawhub.ai/user/yb0554) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to generate a small monitoring service for authorized websites, persist status and latency data, and produce daily availability reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring targets without authorization can create privacy, compliance, or acceptable-use issues. <br>
Mitigation: Use the generated monitor only for websites and services you are authorized to monitor. <br>
Risk: Internal, localhost, metadata-service, or sensitive private endpoints may expose data or network behavior if monitored accidentally. <br>
Mitigation: Review configured URLs before running checks and include sensitive private endpoints only when monitoring them is deliberate. <br>
Risk: Stored reports and retained monitoring history may reveal service availability patterns or endpoint details. <br>
Mitigation: Store generated reports and data files in private locations and review the 90-day retention setting for the deployment. <br>
Risk: Docker or systemd persistence can keep recurring checks running unattended. <br>
Mitigation: Enable unattended persistence only when continuous background monitoring is intended and operationally approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yb0554/website-monitor-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python, JSON, shell, systemd, and Docker code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a configurable monitoring project with SQLite persistence, daily HTML reports, and optional unattended execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
