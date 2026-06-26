## Description: <br>
Helps an agent read recent messages in Windows PC WeChat, draft short Chinese replies, send text or media, capture latest image previews, and use a local daemon for faster repeated replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pddsa](https://clawhub.ai/user/pddsa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using Codex on a Windows desktop use this skill to operate their logged-in PC WeChat: locate chats, read recent messages with OCR, draft context-fit Chinese replies, and send text, images, videos, or files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent powerful control over private WeChat conversations. <br>
Mitigation: Install only when this behavior is intended, and review recipients, message text, and file paths before sending. <br>
Risk: Background daemon, screenshot, and auto-reply behavior can continue operating beyond a single reply task. <br>
Mitigation: Use the daemon only for active reply sessions, avoid sensitive chats, and stop the daemon when finished. <br>
Risk: Smart-reply behavior may send chat text to the configured LLM provider. <br>
Mitigation: Do not use smart-reply unless sharing chat text with that provider is acceptable. <br>


## Reference(s): <br>
- [Fast Reply Workflow](references/fast-reply-workflow.md) <br>
- [OCR and Window Rules](references/ocr-and-window-rules.md) <br>
- [Reply Style Guide](references/reply-style-guide.md) <br>
- [Runtime Requirements](references/runtime-requirements.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language replies with command invocations and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send messages or files through a logged-in local WeChat session when invoked by the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
