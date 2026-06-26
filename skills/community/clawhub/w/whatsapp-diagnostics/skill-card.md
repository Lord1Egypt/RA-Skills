## Description: <br>
Diagnose and fix WhatsApp connectivity issues for OpenClaw agents when a PA is not responding, WhatsApp shows connected but messages do not arrive, the agent is online but not replying, or a new agent setup needs troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw WhatsApp channel failures, separate connection, ingest, and runtime issues, and decide when to escalate to a platform administrator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional API-key checks make live outbound requests using provider credentials. <br>
Mitigation: Run the checks only in a trusted shell and redact API keys, HTTP traces, and related command output before sharing logs. <br>
Risk: Gateway restart commands can affect shared OpenClaw infrastructure. <br>
Mitigation: Coordinate restarts with the responsible platform administrator when multiple agents or shared services may be affected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/whatsapp-diagnostics) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a decision tree and an optional shell health-check script; API-key checks perform live outbound requests when run.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
