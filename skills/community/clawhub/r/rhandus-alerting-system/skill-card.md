## Description: <br>
Centralized alerting and notification system for OpenClaw with multi-channel alerts, rules, escalation, and audit support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhanxerox](https://clawhub.ai/user/rhanxerox) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to configure alert monitoring, trigger notifications, review alert status, and integrate alerting with other OpenClaw skills or operational workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration script can write files into other skill directories and install a recurring cron job. <br>
Mitigation: Review integration and cron commands before running them, approve target paths explicitly, and run the skill in an isolated workspace or least-privilege account. <br>
Risk: Some alert, email, and HTTP monitoring paths build shell commands from alert data, recipient settings, or URLs. <br>
Mitigation: Prefer native HTTP and email APIs or argument-array subprocess calls, and validate or restrict all URLs, alert text, account values, and recipients before execution. <br>
Risk: Notifications may expose sensitive endpoint, incident, or operational details through email, Telegram, or logs. <br>
Mitigation: Redact secrets and sensitive payload fields, use approved recipients and channels, and avoid email alerts for sensitive data until redaction is implemented. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/rhanxerox/rhandus-alerting-system) <br>
- [Publisher profile](https://clawhub.ai/user/rhanxerox) <br>
- [Publisher website](https://tiklick.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript configuration examples; runtime commands emit text and JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create alert records, logs, integration files, notifications, and optional recurring monitoring when installed and run.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md metadata, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
