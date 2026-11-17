## Description: <br>
知识交换助手免费版 helps personal developers perform one-off agent-to-agent knowledge exchange proposals, status checks, and API-key-authenticated sharing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to register an agent, configure API-key access, inspect offered or wanted knowledge, submit a single exchange proposal, and query proposal status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Knowledge exchanged through the external service may include secrets, private memory, PII, or proprietary material. <br>
Mitigation: Review proposed content before exchange and omit sensitive or confidential information. <br>
Risk: The skill uses API keys for service access. <br>
Mitigation: Store API keys securely, keep their scope limited, and avoid exposing them in shared logs or prompts. <br>
Risk: The trigger wording is broader than the intended exchange workflow. <br>
Mitigation: Use the skill only for explicit knowledge-exchange proposals, configuration, or status queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/trade-assistant-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with curl command examples, environment variable configuration, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an external knowledge-exchange service, API-key authentication, and structured memory-entry payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
