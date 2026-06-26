## Description: <br>
Controls XiaoAI speakers through Home Assistant and Xiaomi Miot for text-to-speech, text command execution, URL audio playback, and optional XiaoAI-to-OpenClaw voice bridging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[believe3344](https://clawhub.ai/user/believe3344) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced smart-home users use this skill to route OpenClaw requests to XiaoAI speakers through Home Assistant for announcements, device-oriented text commands, and audio playback. Users who enable the optional bridge can forward whitelisted XiaoAI voice requests back to OpenClaw main for handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional bridge can forward XiaoAI-originated text without built-in authentication. <br>
Mitigation: Run it only on a trusted, firewalled host; bind it to localhost or a private interface; add authentication before wider exposure; and keep whitelist rules restrictive. <br>
Risk: Voice-derived or Home Assistant conversation text may be saved locally and forwarded to OpenClaw main. <br>
Mitigation: Avoid sending sensitive speech through the bridge, review local logs and status files, and set retention or cleanup practices that match the deployment's privacy needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/believe3344/xiaoai-ha-control) <br>
- [Bridge setup guide](references/bridge-setup.md) <br>
- [Home Assistant installation](https://www.home-assistant.io/installation/) <br>
- [HACS installation](https://www.hacs.xyz/docs/use/download/download/) <br>
- [Xiaomi Miot integration](https://github.com/al-one/hass-xiaomi-miot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Home Assistant service calls and optionally forward whitelisted voice text to OpenClaw main when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
