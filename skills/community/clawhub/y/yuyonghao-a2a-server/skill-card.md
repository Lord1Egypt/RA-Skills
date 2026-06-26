## Description: <br>
A WebSocket-based agent-to-agent communication server and client for agent registration, low-latency message forwarding, RPC calls, publish/subscribe channels, capability discovery, heartbeats, and offline message queues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run a local WebSocket hub that lets multiple agents register, discover each other by capability, exchange direct messages, perform RPC-style calls, and broadcast channel events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release enables unauthenticated agent RPC, discovery, and message forwarding. <br>
Mitigation: Use it only on localhost or fully trusted networks unless authentication, authorization, TLS or WSS, identity binding, and message signing are enforced externally. <br>
Risk: Agent identifiers can be registered or overwritten by another connection. <br>
Mitigation: Run only with trusted agents, isolate the server from untrusted clients, and add identity checks before allowing shared or network-accessible deployments. <br>
Risk: Offline messages are stored in memory and delivered later without durable persistence. <br>
Mitigation: Treat queued messages as best-effort local state, avoid sensitive payloads, and add a durable encrypted queue if reliability or confidentiality is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuyonghao-123/yuyonghao-a2a-server) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Test status](artifact/TEST-STATUS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local server and client usage patterns, environment variables, and API examples.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
