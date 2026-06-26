## Description: <br>
Provides common Pugoing central-control platform API calls for querying areas, hosts, and devices, and for controlling devices with natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[run02](https://clawhub.ai/user/run02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent call common Pugoing platform endpoints for area, host, and device discovery, then prepare or execute device-control requests through the bundled Python client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The client can send the configured API key to arbitrary URLs if a request spec uses the full-url option. <br>
Mitigation: Prefer relative path specs, point PUGOING_BASE_URL only at a trusted Pugoing server, and avoid user-supplied full URLs. <br>
Risk: Device-control endpoints can trigger real-world actions without clear safeguards. <br>
Mitigation: Require confirmation of host, device, and intended action before allowing control commands. <br>
Risk: PUGOING_API_KEY is a secret used for authenticated platform calls. <br>
Mitigation: Store the key in the environment, keep request specs under user control, and avoid logging or sharing secret-bearing headers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/run02/pugoing-smart) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/run02) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON request specs passed by file or stdin; API responses may be JSON, text, or event-stream text collected into JSON output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
