## Description: <br>
HTTP API server that exposes OpenClaw agent status for Tidbyt LED displays, returning JSON with agent status, emoji, activity level, and task counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MrScoutsHub](https://clawhub.ai/user/MrScoutsHub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to expose local agent activity through a status API and display it on a Tidbyt 64x32 LED device or related dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local status API can expose agent status and activity details to any client that can reach the configured host and port. <br>
Mitigation: Run it only on a trusted LAN, avoid exposing port 8765 to the internet, and restrict firewall access where possible. <br>
Risk: Background or systemd mode keeps the API running continuously. <br>
Mitigation: Use continuous service mode only when persistent display access is desired, and stop or disable the service when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MrScoutsHub/tidbyt-status) <br>
- [Publisher profile](https://clawhub.ai/user/MrScoutsHub) <br>
- [Tidbyt Pixlet releases](https://github.com/tidbyt/pixlet/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API examples, bash commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operation guidance for a local HTTP status API that emits JSON for Tidbyt display clients.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
