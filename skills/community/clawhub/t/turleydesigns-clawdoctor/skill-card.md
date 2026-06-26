## Description: <br>
Self-healing monitor for OpenClaw gateways, crons, and agent sessions. Use when you need to watch if OpenClaw is running, get Telegram alerts on failures, auto-restart the gateway, detect missed crons or stuck sessions, or monitor token costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RelayPlane](https://clawhub.ai/user/RelayPlane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams running OpenClaw agents use ClawDoctor to monitor gateway, cron, session, auth, budget, and cost health, receive Telegram alerts, and apply configured recovery actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local daemon can take disruptive actions against OpenClaw operations when healing is enabled. <br>
Mitigation: Run in dry-run mode first and enable automatic healing only after confirming the configured actions are appropriate for the target environment. <br>
Risk: Telegram approval callbacks can trigger disruptive actions without verifying the Telegram user or chat that clicked them. <br>
Mitigation: Keep Telegram bot tokens private, restrict who can access approval messages, and avoid enabling Heal auto-fix on production systems until callback authorization is addressed. <br>
Risk: Alerting depends on Telegram credentials and local configuration stored on the host. <br>
Mitigation: Limit access to the host configuration directory and rotate credentials if the Telegram token or chat configuration may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RelayPlane/turleydesigns-clawdoctor) <br>
- [ClawDoctor website](https://clawdoctor.dev) <br>
- [ClawDoctor docs](https://clawdoctor.dev/docs) <br>
- [npm package](https://www.npmjs.com/package/clawdoctor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include local daemon commands, dry-run usage, alert setup, service installation, status checks, logs, and remediation steps.] <br>

## Skill Version(s): <br>
0.4.13 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
