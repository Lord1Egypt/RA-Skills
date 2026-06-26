## Description: <br>
Transpile quantum circuits between Qiskit OpenQASM and OriginIR, run IBC multi-agent consensus, validate OriginIR, and submit circuits to simulator or Wukong quantum hardware through the Quantum Bridge API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adjusternwachukwu-bot](https://clawhub.ai/user/adjusternwachukwu-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert quantum circuits between OpenQASM and OriginIR, validate OriginIR, run multi-agent consensus, check backends, and submit quantum jobs. It is useful when an agent needs API-guided commands or responses for Quantum Bridge workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Circuit files, OriginIR, consensus JSON, and API keys may be sent to the Quantum Bridge remote API. <br>
Mitigation: Review data before submission, avoid sending sensitive circuit or agent data unless approved, and keep QUANTUM_BRIDGE_KEY private. <br>
Risk: Some API operations spend credits or submit work to simulator or Wukong hardware. <br>
Mitigation: Require explicit user approval before operations that upload data, spend credits, or submit quantum jobs. <br>
Risk: Remote execution results depend on the Quantum Bridge service and selected backend availability. <br>
Mitigation: Check available backends and task status before relying on submitted job results. <br>


## Reference(s): <br>
- [Quantum Bridge ClawHub Page](https://clawhub.ai/adjusternwachukwu-bot/quantum-bridge) <br>
- [Quantum Bridge API](https://quantum-api.gpupulse.dev) <br>
- [Quantum Bridge API v1](https://quantum-api.gpupulse.dev/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, API request examples, JSON responses, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated curl commands, qbridge CLI usage, OriginIR or OpenQASM snippets, task polling guidance, and backend or credit information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
