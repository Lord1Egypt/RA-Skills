## Description: <br>
OpenClaw homepage plugin that lets visitors chat with an AI assistant on a personal homepage while separating conversations by session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YaoYi001](https://clawhub.ai/user/YaoYi001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Homepage operators and developers use this skill to expose an OpenClaw agent as a local HTTP chat service for visitors. It supports setup, service control, testing, and session-based conversation continuity for public-purpose agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service exposes an agent-backed HTTP interface with weak authentication behavior. <br>
Mitigation: Bind the service to localhost or place it behind real authentication before deployment. <br>
Risk: Session data can expose visitor conversation history. <br>
Mitigation: Remove or protect the sessions endpoint, validate session IDs, and use only a public-purpose agent with limited privileges. <br>
Risk: Token-bearing gateway URLs may be written to logs. <br>
Mitigation: Stop logging token-bearing URLs and rotate exposed credentials before using the service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YaoYi001/skill-fixon-homepage) <br>
- [Publisher profile](https://clawhub.ai/user/YaoYi001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, HTTP examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local service setup and operation guidance for a homepage chat bridge.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
