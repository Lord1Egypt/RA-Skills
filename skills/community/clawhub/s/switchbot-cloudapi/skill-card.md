## Description: <br>
Control and query SwitchBot devices through the official OpenAPI v1.1, including device listing, status checks, device commands, family and room information, and scene management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[switchbot-dev](https://clawhub.ai/user/switchbot-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home operators use this skill to let an agent inspect and operate SwitchBot devices, rooms, homes, and scenes through authenticated OpenAPI calls. It is intended for accounts where the user is comfortable granting the agent control over connected devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue high-impact smart-home commands, including unlocking doors, opening garages, executing scenes, and managing entry passcodes. <br>
Mitigation: Require explicit human confirmation before unlock, open, scene execution, or passcode create/delete actions, and use it only with SwitchBot accounts where this level of agent control is acceptable. <br>
Risk: SwitchBot API tokens and secrets grant account-level access if exposed. <br>
Mitigation: Store SWITCHBOT_TOKEN and SWITCHBOT_SECRET in protected environment variables, do not hard-code them, and avoid logging them in command output or troubleshooting notes. <br>
Risk: Image upload commands can send private image URLs or Base64 image data to SwitchBot. <br>
Mitigation: Upload image URLs or image data only when the user intends to share that content with SwitchBot. <br>
Risk: Some direct commands are not supported by all device models and may fail or require scenes. <br>
Mitigation: Check device support and command responses, use the CLI preflight behavior for Bluetooth devices, and fall back to SwitchBot scenes when direct OpenAPI commands are unavailable. <br>


## Reference(s): <br>
- [SwitchBot OpenAPI Skill Page](https://clawhub.ai/switchbot-dev/switchbot-cloudapi) <br>
- [SwitchBot OpenAPI endpoint](https://api.switch-bot.com) <br>
- [Commands reference](references/commands.md) <br>
- [Usage examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API payloads, and command output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and API-call guidance that require SWITCHBOT_TOKEN and SWITCHBOT_SECRET, and may return JSON from SwitchBot OpenAPI endpoints.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
