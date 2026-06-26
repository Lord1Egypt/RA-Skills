## Description: <br>
Sends Enterprise WeChat webhook messages in text, Markdown, Markdown V2, image, and news formats, including chunking for long text-like messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxf8126275](https://clawhub.ai/user/wxf8126275) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams can use this skill to send status updates, deployment notices, reminders, screenshots, and article-style notifications to Enterprise WeChat group robots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URLs can grant posting access to Enterprise WeChat groups and should be treated as secrets. <br>
Mitigation: Store webhook URLs outside prompts and shared logs, rotate exposed URLs, and verify the destination before sending. <br>
Risk: The skill can transmit arbitrary message text and local or remote image contents to a webhook destination. <br>
Mitigation: Review outgoing content, avoid credentials or sensitive local files, and restrict image inputs to trusted files or approved URLs. <br>
Risk: Text messages default to mentioning all recipients. <br>
Mitigation: Make mass mentions opt-in or remove @all defaults before routine use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxf8126275/qywx-send-skill) <br>
- [Enterprise WeChat webhook API documentation](https://developer.work.weixin.qq.com/document/path/99110) <br>
- [Webhook send message API](https://developer.work.weixin.qq.com/document/path/90236) <br>
- [Message type documentation](https://developer.work.weixin.qq.com/document/path/90237) <br>
- [Bundled API documentation](references/api_documentation.md) <br>
- [Bundled usage examples](references/usage_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Enterprise WeChat webhook payloads and command or Python usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text, markdown, markdown_v2, image, and news messages; long text-like messages may be split into multiple webhook sends.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
