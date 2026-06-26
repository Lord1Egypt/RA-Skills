## Description: <br>
Sends a concise WeChat task summary and the full report by QQ Mail when the user asks to push a report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu99012101-bot](https://clawhub.ai/user/liu99012101-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to distribute generated analysis reports through two channels: a short structured WeChat summary and the full report by QQ Mail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses QQ Mail SMTP credentials and a push-service token, and report content leaves the user's environment. <br>
Mitigation: Install only where those credentials and report contents are acceptable to share with the configured mail and push services. <br>
Risk: The security guidance flags the PushPlus endpoint as using HTTP. <br>
Mitigation: Change the push endpoint to HTTPS before using the skill for sensitive reports. <br>
Risk: The skill can send report content to external channels after user-triggered execution. <br>
Mitigation: Require explicit confirmation for each send, especially when reports contain sensitive or proprietary information. <br>
Risk: The artifact instructions reference scripts/push_report.py, while the bundled script path is scripts/ush_report.py. <br>
Mitigation: Fix the script path mismatch before relying on the documented command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu99012101-bot/report-push-wechat-qqmail) <br>
- [Publisher profile](https://clawhub.ai/user/liu99012101-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, JSON] <br>
**Output Format:** [Markdown or plain-text report content, a short WeChat summary, a shell command invocation, and JSON delivery status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, QQ Mail SMTP credentials, a target QQ Mail address, and WECHAT_PUSH_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
