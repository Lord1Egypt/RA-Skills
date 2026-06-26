## Description: <br>
Send Web Push notifications from a Node.js backend using the web-push npm library with VAPID authentication and payload encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to configure browser Push API subscriptions, manage VAPID keys, and send encrypted Web Push notifications from Node.js services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VAPID private keys, GCM API keys, push endpoints, and subscription auth values are sensitive credentials. <br>
Mitigation: Store credentials in environment variables or a secrets manager, avoid committing real values, and rotate any credential exposed in prompts or logs. <br>
Risk: Notification sends can contact third-party browser push services and reach real end users. <br>
Mitigation: Use test subscriptions before production sends, validate recipients and payloads, and limit access to production subscription data. <br>


## Reference(s): <br>
- [web-push Complete API Reference](references/webpush.md) <br>
- [ClawHub Web Push Notifications release](https://clawhub.ai/openlark/web-push) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples using VAPID keys, PushSubscription JSON, and environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
