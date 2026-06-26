## Description: <br>
Install and connect the WeChat ClawBot channel plugin for OpenClaw, including a qrcode-terminal patch that emits scannable QR image links for chat surfaces where ASCII QR codes are unreliable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaojiankui](https://clawhub.ai/user/shaojiankui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, connect, and troubleshoot the WeChat ClawBot channel plugin for OpenClaw. It provides setup commands, QR login guidance, accountId mismatch remediation, and optional per-channel session configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat login QR contents can be embedded in a URL handled by the third-party api.qrserver.com QR image service. <br>
Mitigation: Use a real terminal or local/offline QR renderer when QR contents should not be sent to a third-party service. <br>
Risk: The skill installs @tencent-weixin/openclaw-weixin-cli@latest, which can change behavior between runs. <br>
Mitigation: Verify the npm package and pin or review the version before running the install command in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaojiankui/weixin-setup) <br>
- [QR Server image endpoint used by the patch](https://api.qrserver.com/v1/create-qr-code/?size=400x400&data=) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that install an OpenClaw WeChat plugin, patch qrcode-terminal, verify status, and adjust OpenClaw channel configuration.] <br>

## Skill Version(s): <br>
5.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
