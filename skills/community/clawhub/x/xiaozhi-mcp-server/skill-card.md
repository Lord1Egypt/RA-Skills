## Description: <br>
Connects a Xiaozhi smart speaker to OpenClaw so spoken requests can be processed by OpenClaw and read aloud by the device. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elegant1998](https://clawhub.ai/user/elegant1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to bridge Xiaozhi voice-device requests into OpenClaw agent tasks and return short spoken results. It is intended for voice-assistant workflows such as weather checks, document drafting, information lookup, and task status retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service exposes broad agent control through a token-protected network endpoint. <br>
Mitigation: Keep port 28765 on a trusted LAN or protect it with TLS, VPN, or reverse proxy controls; treat the token like a password and rotate it if exposed. <br>
Risk: The artifact ships with a prefilled target_session. <br>
Mitigation: Edit config.yaml before installation to remove or replace the bundled target_session with the intended destination. <br>
Risk: Spoken requests may contain sensitive information that is relayed through the assistant bridge. <br>
Mitigation: Avoid speaking sensitive secrets and review the configured OpenClaw destination before use. <br>
Risk: The startup script can install Python dependencies directly into the system environment. <br>
Mitigation: Install and run the service in a virtual environment when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elegant1998/xiaozhi-mcp-server) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [README.md](README.md) <br>
- [ESP32 README](esp32/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON-RPC text responses, WebSocket JSON messages, and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Async task IDs and short voice summaries; requires port, token, and target_session configuration.] <br>

## Skill Version(s): <br>
2.0.8 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
