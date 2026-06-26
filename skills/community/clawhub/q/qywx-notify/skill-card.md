## Description: <br>
A skill for sending notifications via WeChat Work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yc-weichao](https://clawhub.ai/user/yc-weichao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to send text, Markdown, and image-linked notifications to WeCom group chats through a robot webhook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URLs and notification contents may appear in local logs or command responses. <br>
Mitigation: Treat the webhook URL like a password, avoid shared logs containing skill output, and rotate the webhook if it may have been exposed. <br>
Risk: Sensitive notification content may be sent to WeCom group chats. <br>
Mitigation: Avoid sending sensitive messages through this version and review message recipients before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, JSON] <br>
**Output Format:** [JSON command results plus WeCom text or Markdown notification payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include image URLs and @all or user mentions; failed sends are retried.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
