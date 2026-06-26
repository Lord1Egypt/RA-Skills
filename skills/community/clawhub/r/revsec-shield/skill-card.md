## Description: <br>
24/7 security monitoring for your OpenClaw agent that detects prompt injection attacks, malicious skills, and data exfiltration attempts, then delivers plain-English alerts when suspicious activity is found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[revupai](https://clawhub.ai/user/revupai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use RevSec Shield to register an OpenClaw agent with RevSec, keep background monitoring active, poll for security alerts, and check recent threat status. It is intended for ongoing monitoring and alert delivery after first-time setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creates persistent background automation that runs every 5 minutes. <br>
Mitigation: Install only when continuous monitoring is intended, and remove the revsec:alert-poll cron job if you stop using the skill. <br>
Risk: Sends local agent metadata, including hostname, model, and skill inventory, to a third-party RevSec service. <br>
Mitigation: Confirm you are comfortable with this metadata sharing before setup and review the RevSec account destination. <br>
Risk: Uses REVSEC_API_KEY for authenticated API access. <br>
Mitigation: Store the key only in the OpenClaw runtime environment and avoid setup steps that print or log the key. <br>


## Reference(s): <br>
- [RevSec Shield on ClawHub](https://clawhub.ai/revupai/revsec-shield) <br>
- [RevSec homepage](https://revsec.revt2d.com) <br>
- [RevSec personal dashboard](https://revsec.revt2d.com/personal) <br>
- [RevSec signup](https://revsec.revt2d.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain-text status or alert messages, with shell commands and configuration snippets during setup or troubleshooting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVSEC_API_KEY and may create a recurring OpenClaw cron job named revsec:alert-poll.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
