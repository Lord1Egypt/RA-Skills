## Description: <br>
Enables OpenClaw agents to discover trusted peers, exchange messages, and coordinate over local UDP networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turfptax](https://clawhub.ai/user/turfptax) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to let OpenClaw agents communicate with approved peers on the same LAN, review message history, and coordinate work through controlled local messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trusted network peers and optional wake-up settings can influence agent behavior by causing incoming messages to be processed as agent turns. <br>
Mitigation: Use the skill only with highly trusted peers, keep hookToken disabled unless needed, and review incoming messages and udp_log regularly. <br>
Risk: The optional relayServer can copy message contents to a monitoring endpoint. <br>
Mitigation: Leave relayServer disabled unless you control the endpoint and accept that sent and received message contents may be copied there. <br>
Risk: LAN messaging can expose sensitive project details if agents send file contents, secrets, or private data. <br>
Mitigation: Confirm with the user before sending project details and avoid sharing credentials or private data unless explicitly instructed. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/turfptax/openclaw-udp-messenger) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/turfptax/udp-messenger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing guidance for UDP peer discovery, messaging, trust management, logging, and runtime configuration.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
