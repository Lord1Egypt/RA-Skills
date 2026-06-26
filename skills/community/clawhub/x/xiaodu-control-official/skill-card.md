## Description: <br>
Helps an agent configure, verify, troubleshoot, and control XiaoDu smart screen and XiaoDu IoT MCP workflows, including token-based setup, device listing, text speech, voice commands, camera capture, media push, appliance control, and scene triggering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dueros-mcp](https://clawhub.ai/user/dueros-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to XiaoDu smart screens and IoT devices through mcporter, then run bounded device-control, media, scene, and troubleshooting workflows. It is intended for users who trust the skill with a XiaoDu access token and real smart-home actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a XiaoDu AccessToken that can be stored in mcporter configuration. <br>
Mitigation: Treat the token as a secret, do not echo it back to users, and review permissions on ~/.mcporter/mcporter.json after setup. <br>
Risk: The skill can trigger smart-home devices, scenes, locks, appliances, and camera capture in private spaces. <br>
Mitigation: Require explicit user confirmation before camera use, scene triggers, locks, batch appliance changes, or actions that could affect people or a private space. <br>
Risk: Device capabilities vary by live XiaoDu IoT schema and device availability. <br>
Mitigation: Check available devices and schema before control actions, and refuse unsupported or missing-device requests instead of guessing parameters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dueros-mcp/xiaodu-control-official) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dueros-mcp) <br>
- [Clawdis homepage](https://github.com/dueros-mcp/xiaodu-control) <br>
- [Capability boundaries](references/capability-boundaries.md) <br>
- [Command patterns](references/command-patterns.md) <br>
- [Install for users](references/install-for-users.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and script-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce mcporter commands and configuration steps that interact with XiaoDu smart screens and IoT devices.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
