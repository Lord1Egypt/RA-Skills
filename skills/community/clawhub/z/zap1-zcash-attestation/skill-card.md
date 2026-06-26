## Description: <br>
Provides Zcash-anchored attestation for agent messages, commands, session events, lifecycle events, proof verification, and policy-related audit records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skndrs](https://clawhub.ai/user/skndrs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to attach a verifiable audit trail to agent activity, inspect ZAP1 proof status, and query attestation records. It is most relevant for agents that need external proof checkpoints or policy-related accountability records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can continuously send hashes of agent activity to a remote attestation service, creating a persistent external audit trail. <br>
Mitigation: Install only when that audit trail is intended, use a trusted or self-hosted apiUrl, and set proofInterval to 0 if checkpoint messages are unwanted. <br>
Risk: Write operations and API-key provisioning can use configured credentials, including administrative credentials if supplied. <br>
Mitigation: Use a least-privilege ZAP1 key and avoid configuring admin credentials unless key provisioning is explicitly required. <br>
Risk: Policy rules are not a standalone enforcement guarantee unless the host agent wires the policy evaluator into tool execution. <br>
Mitigation: Confirm the host agent invokes evaluatePolicy before relying on blockedTools or restrictedTools for execution control. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/skndrs/zap1-zcash-attestation) <br>
- [ZAP1 protocol](https://github.com/Frontier-Compute/zap1) <br>
- [ZAP1 protocol specification](https://github.com/Frontier-Compute/zap1/blob/main/ONCHAIN_PROTOCOL.md) <br>
- [ZAP1 verifier](https://pay.frontiercompute.io/verify.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration guidance] <br>
**Output Format:** [JSON API responses, checkpoint text, and Markdown configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit proof checkpoints into agent messages when configured; read-only tools work without an API key, while attestation and administrative actions require credentials.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
