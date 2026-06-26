## Description: <br>
ClawDoctor is a self-healing doctor for OpenClaw that monitors gateway, crons, sessions, auth, and costs, sends Telegram alerts, and can auto-restart the gateway when it goes down. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RelayPlane](https://clawhub.ai/user/RelayPlane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators running OpenClaw in production use ClawDoctor to monitor gateway, cron, session, auth, and cost health, receive Telegram alerts, and optionally recover by restarting the gateway when it appears down. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitoring daemon reads OpenClaw operational files and stores local event history. <br>
Mitigation: Install only in environments where this local monitoring is acceptable, and review file access expectations before enabling the daemon. <br>
Risk: Telegram alerts can send operational details outside the local machine. <br>
Mitigation: Use a dedicated Telegram bot token and chat, and confirm alert contents are appropriate for the deployment. <br>
Risk: Auto-fix mode can restart the OpenClaw gateway automatically. <br>
Mitigation: Start with dry-run mode and enable auto-fix only where automatic gateway restarts are acceptable. <br>


## Reference(s): <br>
- [ClawDoctor ClawHub listing](https://clawhub.ai/RelayPlane/relayplane-clawdoctor) <br>
- [ClawDoctor website](https://clawdoctor.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include install commands, daemon commands, dry-run guidance, alert behavior, and local configuration details.] <br>

## Skill Version(s): <br>
0.4.11 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
