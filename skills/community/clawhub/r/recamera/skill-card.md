## Description: <br>
reCameraV2 provides a reCamera (RV1126B) Web API reference for authentication, device management, media configuration, recording and storage, AI inference, terminal and log access, and SenseCraft cloud model conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjq2020](https://clawhub.ai/user/mjq2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build, debug, and operate integrations with reCamera devices and SenseCraft AI services. It helps agents construct authenticated HTTP and WebSocket calls, follow device-specific configuration workflows, and look up endpoint schemas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through network scanning and powerful reCamera device-control workflows. <br>
Mitigation: Use it only for reCamera devices and networks the user owns or is authorized to manage, and require clear confirmation before scans or device-control actions. <br>
Risk: Authenticated workflows may expose passwords, cookies, tokens, logs, or proprietary model files. <br>
Mitigation: Avoid exposing secrets or sensitive artifacts in outputs, redact logs when appropriate, and keep tokens scoped to the active session. <br>
Risk: Resets, firmware changes, storage formatting, file deletion, terminal access, and configuration writes can disrupt devices or data. <br>
Mitigation: Require explicit user confirmation before these actions and follow the documented read-before-write pattern for configuration updates. <br>


## Reference(s): <br>
- [API_REFERENCE.md](artifact/API_REFERENCE.md) <br>
- [ClawHub skill page](https://clawhub.ai/mjq2020/recamera) <br>
- [SenseCraft training API](https://sensecraft-train-api.seeed.cc) <br>
- [SenseCraft authorization endpoint](https://sensecraft.seeed.cc/ai/authorize?client_id=seeed_recamera&response_type=token&scop=profile&redirec_url={your_url}) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with HTTP endpoint references, JSON examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated HTTP/WebSocket call guidance for authorized reCamera devices and SenseCraft AI services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
