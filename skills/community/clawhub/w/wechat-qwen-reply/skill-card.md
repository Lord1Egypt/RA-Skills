## Description: <br>
WeChat chat reader + auto-reply (Qwen-VL vision + AHK send). Supports fast/slow capture, group nickname labels, file/red-packet cards, and filtering system messages on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenxundaozu](https://clawhub.ai/user/chenxundaozu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows automation users use this skill to capture WeChat chat screenshots, send them to Qwen-VL for transcription, and prepare chat text for reply workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private WeChat screenshots may be sent to DashScope/Qwen-VL. <br>
Mitigation: Use the skill only on chats that are allowed to be shared with the external model provider. <br>
Risk: Referenced PowerShell capture scripts and AHK send automation are not present in the artifact for review. <br>
Mitigation: Inspect or obtain those scripts before installation or execution. <br>
Risk: Message-sending automation could post unintended replies. <br>
Mitigation: Require manual confirmation before any automated message is sent. <br>
Risk: The script uses a hardcoded personal API-key path. <br>
Mitigation: Replace it with a properly scoped secret path or environment-based secret handling before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenxundaozu/wechat-qwen-reply) <br>
- [DashScope compatible-mode chat completions endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text chat transcript with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the latest recognized chat text and debug crop image to local files when run as documented.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
