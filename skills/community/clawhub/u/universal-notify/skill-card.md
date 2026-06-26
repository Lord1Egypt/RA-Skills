## Description: <br>
Send notifications through multiple channels with a single script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JosunLP](https://clawhub.ai/user/JosunLP) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to send alerts, monitoring notifications, deployment notices, and other event messages through a recipient's preferred notification channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification text is sent to the selected external or self-hosted service and could expose sensitive personal or internal data. <br>
Mitigation: Use trusted endpoints, avoid secrets or sensitive data in messages, and prefer approved or self-hosted channels for sensitive alerts. <br>
Risk: Some channels require tokens or credentials that may be passed on the command line. <br>
Mitigation: Protect notification credentials and avoid exposing tokens in shell history, logs, or shared terminal sessions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces notification-send commands for ntfy.sh, Gotify, generic webhooks, email, Telegram Bot API, and Pushover.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
