## Description: <br>
Instructs the OpenClaw Agent on how to interact securely with other agents by requiring cryptographic authentication before right-of-way yielding or sensor federation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to coordinate multi-agent physical interactions, including authenticated peer handshakes, sensor federation decisions, and right-of-way arbitration. It is intended for OpenClaw agent workflows that need to reject unauthenticated peer broadcasts before changing trajectory or incorporating shared sensor data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill claims PKI-backed security while the executable only checks a hard-coded signature before enabling robot coordination decisions. <br>
Mitigation: Do not deploy in real robot, drone, vehicle, or other safety-sensitive environments until real mutual authentication, signed messages, replay protection, encrypted channels, and explicit authorization replace the placeholder signature check. <br>
Risk: Authenticated messages can trigger right-of-way decisions such as yielding, torque braking, and sensor-data integration. <br>
Mitigation: Require human and system safety review, bounded actuation policies, and independent fail-safe controls before allowing outputs to affect physical movement. <br>
Risk: Federated sensor sharing may expose or incorporate peer sensor data across agents. <br>
Mitigation: Define privacy controls, data minimization, and trust boundaries for any P2P sensor federation before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-swarm-sync-protocol) <br>
- [S2-SWM Special Protocol Whitepaper](artifact/S2_SWM_Special_Protocol_Whitepaper.md) <br>
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Configuration] <br>
**Output Format:** [Markdown instructions and JSON tool-call responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires S2_SWARM_PKI_ROOT for the advertised authentication configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, package.json, openclaw.plugin.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
