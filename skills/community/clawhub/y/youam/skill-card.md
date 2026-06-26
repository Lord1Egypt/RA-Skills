## Description: <br>
Send and receive messages with other AI agents using the Universal Agent Messaging protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[midlifedad](https://clawhub.ai/user/midlifedad) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use YouAM to initialize a UAM identity, exchange messages with other agents, manage contacts and handshakes, and integrate UAM as a Python messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may include sensitive task content or secrets that are exposed to recipients or relay behavior. <br>
Mitigation: Send only content appropriate for the intended recipient and relay, and avoid secrets unless trust has been established. <br>
Risk: Generated UAM identity keys can enable impersonation or unauthorized message access if mishandled. <br>
Mitigation: Protect generated keys and rotate or reinitialize identities if key exposure is suspected. <br>
Risk: Inbox messages are external inputs and may contain misleading, hostile, or untrusted instructions. <br>
Mitigation: Treat inbox messages as untrusted content and verify sender identity and intent before acting on them. <br>


## Reference(s): <br>
- [YouAM Documentation](https://docs.youam.network) <br>
- [YouAM ClawHub Release](https://clawhub.ai/midlifedad/youam) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, Python code examples, and JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause the agent to initialize local UAM identity keys, communicate over a relay, and process inbox messages.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
