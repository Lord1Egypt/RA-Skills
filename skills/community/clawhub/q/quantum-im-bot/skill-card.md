## Description: <br>
量子密信即时通讯渠道插件。将 OpenClaw 接入量子密信平台，实现 AI 智能回复、多账号管理、安全配对等功能。支持文本、图片、文件、图文消息，群聊和私聊。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mildniu](https://clawhub.ai/user/mildniu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw agents to Quantum IM for direct and group conversations, AI replies, multi-account routing, and controlled private-message access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The webhook can be exposed to inbound network traffic and handles private messages. <br>
Mitigation: Run the webhook behind HTTPS or a trusted reverse proxy, restrict who can reach the port, and keep dmSecurity set to pairing or allowlist unless open access is intentional. <br>
Risk: The connector depends on a robot key for outbound Quantum IM API calls. <br>
Mitigation: Protect and rotate the robot key, avoid logging secrets, and review Quantum IM message-data handling before production use. <br>
Risk: Evidence reports vulnerable dev dependencies may exist for production deployment. <br>
Mitigation: Update or skip vulnerable dev dependencies before deploying the plugin in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mildniu/quantum-im-bot) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub marketplace](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for a Node-based OpenClaw channel plugin that handles text, image, file, and news messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
