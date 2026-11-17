## Description:

WeChat chat reader + auto-reply (Qwen-VL vision + AHK send). Supports fast/slow capture, group nickname labels, file/red-packet cards, and filtering system messages on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxundaozu](https://clawhub.ai/user/chenxundaozu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill on Windows to capture WeChat chat screenshots, send them to Qwen-VL through DashScope, and return recognized chat text for review or reply workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private WeChat screenshots are sent to DashScope for processing.

Mitigation: Use only with conversations appropriate for third-party processing, and avoid confidential personal, business, payment, or account chats.

Risk: Recognized chat text and the latest cropped screenshot are saved in the local workspace.

Mitigation: Review local retention expectations and remove saved outputs when they are no longer needed.

Risk: The workflow depends on unbundled PowerShell and AHK scripts that can control capture or sending behavior.

Mitigation: Verify those external scripts before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenxundaozu/skills/wechat-qwen-reply)
- [DashScope Compatible Chat Completions Endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text chat transcript printed to stdout and saved to a local text file, with optional debug screenshot output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, WeChat PC, AHK v2, Python 3.12, a DashScope API key, and local capture scripts referenced by the package.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
