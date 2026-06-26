## Description: <br>
Automatically watches Telegram group messages that mention a configured bot and forwards the cleaned message text to a configured QQ private chat through OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to bridge selected Telegram group messages into QQ private chat workflows. It is intended for configured chat-forwarding automation where participants understand that message content may be relayed between services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the bridge reads local session transcripts and forwards chat content, which can expose messages to another service. <br>
Mitigation: Limit the configured session file and QQ target to the intended chat scope, and obtain consent from users whose Telegram content may be bridged. <br>
Risk: The release security guidance identifies a local command-injection risk in the forwarding command path. <br>
Mitigation: Review before installation and replace shell command construction with argument-based spawn/execFile or a native messaging API before running with trusted OpenClaw credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bg1avd/telegram-qq-bridge) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Forwarded chat text with configuration and command-line setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forwards only messages containing the configured Telegram bot mention, prefixes forwarded content with [Telegram], and relies on local OpenClaw and QQ Bot configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
