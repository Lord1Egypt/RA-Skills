## Description: <br>
Intelligently dispatches WeChat messages by extracting recipients and content, handling text, images, or files with confirmation and selection prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aw11100](https://clawhub.ai/user/aw11100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent resolve WeChat contacts or group chats and prepare text, image, or file messages for sending after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message text, recipient data, media URLs, file URLs, and credentials may be sent to the SynodeAI/WeChat gateway. <br>
Mitigation: Install only when the gateway is trusted, prefer HTTPS, and rotate or replace bundled credentials before use. <br>
Risk: The local bridge can send WeChat messages through a service that the security evidence describes as unauthenticated. <br>
Mitigation: Restrict the service to trusted local access and require a server-side confirmation or allowlist before final sending. <br>
Risk: Ambiguous contact or group matching could target the wrong recipient. <br>
Mitigation: Use the provided choice and confirmation flow before invoking the final send endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aw11100/wechat-new-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON HTTP request and response patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes text, image, and file requests through a local WeChat bridge and an external gateway; final sending depends on confirmation flow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
