## Description: <br>
openclaw-smartpi helps an agent guide SmartPi users through device binding, QR-code setup, device management, connection troubleshooting, and 9002 timeout diagnosis in local OpenClaw environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengseven777](https://clawhub.ai/user/fengseven777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use this skill when a user needs help installing or enabling the openclaw-smartpi plugin, binding a SmartPi device, listing or removing SmartPi devices, checking connection status, reviewing Gateway logs, or diagnosing SmartPi no-response and 9002 timeout issues. <br>

### Deployment Geography for Use: <br>
No deployment geography restriction is stated in the release evidence; use in local OpenClaw environments where SmartPi and the OpenClaw CLI are available. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to run local OpenClaw commands that install plugins, restart the Gateway, remove SmartPi devices, or change configuration. <br>
Mitigation: Require explicit user confirmation before state-changing actions and explain the expected impact before proceeding. <br>
Risk: SmartPi connection or timeout status can be misdiagnosed if the agent relies on assumptions instead of local evidence. <br>
Mitigation: Use OpenClaw command output and Gateway log keywords such as WebSocket connected, WebSocket disconnected, cannot resolve agentId, and AI response timeout before stating a conclusion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengseven777/skills/smartpi) <br>
- [Publisher profile](https://clawhub.ai/user/fengseven777) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Concise troubleshooting steps, command suggestions, status summaries, and configuration snippets.] <br>
**Output Parameters:** [SmartPi device state, OpenClaw CLI output, Gateway log keywords, device identifiers, and user confirmations for state-changing actions.] <br>
**Other Properties Related to Output:** [The skill instructs the agent to base status on observed command output or logs and to pause for confirmation before installing plugins, deleting devices, restarting the Gateway, or changing configuration.] <br>

## Skill Version(s): <br>
1.0.8 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
