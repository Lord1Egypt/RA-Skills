## Description: <br>
Send push notifications to a phone through Pushover for reminders, monitoring alerts, cron summaries, and other out-of-band notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DigitallyBorn](https://clawhub.ai/user/DigitallyBorn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to send Pushover alerts from agent workflows, scheduled jobs, and monitoring or reminder automation. It is useful when a workflow needs an out-of-band phone notification rather than only an in-chat response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification titles, messages, and optional URLs are sent to Pushover. <br>
Mitigation: Avoid sending secrets or sensitive content in notifications, and review automated messages before enabling them. <br>
Risk: Pushover app tokens and user keys can be exposed if passed through shared command lines or committed into workflows. <br>
Mitigation: Use a dedicated Pushover app token and store credentials in environment variables or a secret store. <br>
Risk: Automated alerts can spam recipients, especially when using emergency priority retries. <br>
Mitigation: Review scheduled or monitoring workflows and set emergency retry and expire values deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DigitallyBorn/pushover-notify) <br>
- [Pushover API quick reference](references/pushover-api.md) <br>
- [Pushover API documentation](https://pushover.net/api) <br>
- [Pushover application setup](https://pushover.net/apps/build) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with bash command examples and a bundled Node.js script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Pushover app token and user key; supports optional title, URL, device, sound, priority, timestamp, retry, and expire fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
