## Description: <br>
Sends text, Markdown, image, news, file, and template-card notifications to WeChat Work chats through a configured group robot webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kriouerlia](https://clawhub.ai/user/kriouerlia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow operators use this skill to send operational alerts, scheduled reports, trading signals, and automation notifications into WeChat Work groups or users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured webhook URL is a secret that can send messages into a WeChat Work chat. <br>
Mitigation: Keep the webhook URL out of source control and configure it through a protected environment variable. <br>
Risk: Messages may include sensitive business data or notify all members of a group. <br>
Mitigation: Use a limited-purpose group or bot where possible and review scheduled jobs or automations before enabling them. <br>
Risk: High-frequency scheduled notifications can exceed documented webhook limits or create noisy alerts. <br>
Mitigation: Throttle automation that calls the webhook and keep scheduled intervals above the documented minimum guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kriouerlia/wechat-notify) <br>
- [Publisher profile](https://clawhub.ai/user/kriouerlia) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Python API calls and command-line usage guidance with webhook response dictionaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a WeChat Work webhook URL and the requests Python package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
