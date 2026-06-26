## Description: <br>
Controls a logged-in Windows WeChat client to send text or image messages to specified contacts or groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niansen3-svg](https://clawhub.ai/user/niansen3-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent send text or image updates through a local, logged-in Windows WeChat client for notifications, forwarding, and scheduled reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send real WeChat messages, including bulk messages, from a logged-in local client. <br>
Mitigation: Require a user preview and confirmation before each send, especially for bulk or external-recipient workflows. <br>
Risk: The local HTTP service can enqueue messages if exposed or protected by a weak token. <br>
Mitigation: Keep the service bound to localhost and use a strong private token. <br>
Risk: Logs, clipboard contents, image URLs, recipients, and message text may contain sensitive information. <br>
Mitigation: Treat these values as sensitive, restrict log access, and avoid sending secrets or regulated data. <br>
Risk: Background WPush monitoring can send third-party alerts beyond direct message sending. <br>
Mitigation: Disable WPush monitoring unless the operator explicitly needs external alerting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/niansen3-svg/wechat-automation-api) <br>
- [Skill invocation guide](artifact/SKILL.md) <br>
- [Project README](artifact/README.md) <br>
- [Changelog](artifact/docs/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text, Configuration] <br>
**Output Format:** [Command-line output and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends messages through the user's local WeChat session and returns success or failure status.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
