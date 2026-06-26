## Description: <br>
Monitor websites for uptime, SSL certificate expiry, response time, HTTP errors, and content changes, then generate health reports and alerts when issues are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and site owners use this skill to check website uptime, TLS certificate expiry, response time, HTTP status, and monitoring alerts for domains they control or are authorized to test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local shell-based checks that make network requests to domains supplied by the user. <br>
Mitigation: Use recurring monitoring only for sites the user controls or is authorized to test, and review URLs before running checks. <br>
Risk: Local monitoring configuration and history can reveal monitored domains, outage timing, and operational details. <br>
Mitigation: Store config and history in an appropriate local workspace path, limit access to those files, and avoid recording sensitive targets unnecessarily. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/site-health-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON health-check data and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-site reports, multi-site summaries, alert text, cron suggestions, and local monitoring configuration guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
