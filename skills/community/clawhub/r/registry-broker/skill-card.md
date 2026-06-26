## Description: <br>
Search 72,000+ AI agents across 14 registries, chat with any agent, register your own agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kantorcodes](https://clawhub.ai/user/kantorcodes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to discover AI agents across multiple registries, inspect agent details, start or continue chat sessions, and register their own agents with a broker service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat messages, agent registration payloads, and API keys are sent to the configured Registry Broker service. <br>
Mitigation: Use only trusted broker endpoints, avoid sending secrets or regulated data, and scope REGISTRY_BROKER_API_KEY to the minimum needed access. <br>
Risk: A custom REGISTRY_BROKER_BASE_URL can redirect requests to an untrusted service. <br>
Mitigation: Set REGISTRY_BROKER_BASE_URL only to endpoints the operator controls or has explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kantorcodes/registry-broker) <br>
- [Publisher profile](https://clawhub.ai/user/kantorcodes) <br>
- [Registry Broker website](https://hol.org/registry) <br>
- [Registry Broker API](https://hol.org/registry/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands run through a Node CLI and return JSON to stdout; authenticated operations can use REGISTRY_BROKER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
