## Description: <br>
Connect OpenClaw-style runs to VizClaw live rooms from a ClawHub-installable skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araa47](https://clawhub.ai/user/araa47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create VizClaw rooms and stream OpenClaw-style run events through JSONL, WebSocket, gateway, or log-tail bridges. It supports trigger, agent, tool, skill, heartbeat, reminder, and configuration event visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Run activity may be sent to VizClaw during live visualization. <br>
Mitigation: Use overview mode for sensitive sessions and do not stream secrets or data you are not allowed to share. <br>
Risk: Running the remote script through unpinned uv run can increase supply-chain exposure. <br>
Mitigation: Prefer the ClawHub-installed artifact when installing or running the skill. <br>
Risk: Gateway tokens can be exposed if used over non-local or non-TLS WebSocket endpoints. <br>
Mitigation: Use local gateway endpoints or TLS-protected WebSocket connections when a gateway token is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/araa47/vizclaw) <br>
- [VizClaw connect script](https://vizclaw.com/skills/vizclaw/scripts/connect.py) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON events, guidance] <br>
**Output Format:** [Markdown instructions with bash examples and JSON/WebSocket event payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python >=3.10 and the websockets dependency; overview and hidden modes redact query, tool, and report text.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
