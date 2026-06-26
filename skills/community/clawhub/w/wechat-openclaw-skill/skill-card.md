## Description: <br>
Provides guidance and helper scripts for installing and binding a WeChat channel so users can chat with an OpenClaw assistant from WeChat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ynxiyan](https://clawhub.ai/user/ynxiyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and administrators use this skill to check prerequisites, install the Tencent WeChat OpenClaw plugin, bind a WeChat account by QR code, and troubleshoot the WeChat access channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Binding WeChat creates a persistent access channel to the user's OpenClaw assistant. <br>
Mitigation: Install only when this access channel is intended, bind only trusted accounts, and configure authentication, allowlists, rate limits, and tool approval where available. <br>
Risk: The installation flow uses an unpinned npx command for the Tencent WeChat plugin. <br>
Mitigation: Review the plugin source or package before running the command and prefer a reviewed pinned version when operational policy requires it. <br>
Risk: Messages, files, or images sent through WeChat may reach the assistant channel. <br>
Mitigation: Avoid sending secrets, regulated files, or sensitive data through the channel unless the deployment has appropriate controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ynxiyan/wechat-openclaw-skill) <br>
- [WeChat plugin documentation](https://docs.openclaw.ai/channels/weixin) <br>
- [OpenClaw integration guide](https://docs.openclaw.ai/integration) <br>
- [Bilibili installation tutorial](https://www.bilibili.com/video/BV1mdAgziEkh) <br>
- [Tencent WeChat OpenClaw issues](https://github.com/tencent-weixin/openclaw-weixin/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local environment checks and installation guidance for a WeChat-to-OpenClaw channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
