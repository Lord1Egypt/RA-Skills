## Description: <br>
SA Master Agent helps convert BA business assets into standardized system architecture design documents, interface documentation, deployment implementation guides, and detailed design review reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo21cn](https://clawhub.ai/user/leo21cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and delivery teams use this skill to turn BA or product-manager requirements into architecture design materials and to review detailed designs for architectural consistency. It supports system architecture design, API/interface design, deployment guidance, and detailed design review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Internal architecture documents, prompts, file paths, and generated outputs may be processed by the remote smartmoves.com.cn MCP service. <br>
Mitigation: Use the skill only when the publisher and remote MCP service are trusted, and avoid sensitive project materials unless external processing is acceptable. <br>
Risk: The artifact includes a shared bearer token for the remote MCP service. <br>
Mitigation: Treat the credential as third-party managed, review credential ownership before installation, and rotate or replace it where deployment policy requires controlled credentials. <br>
Risk: Architecture recommendations and review conclusions may be incomplete or unsuitable for a specific system context. <br>
Mitigation: Have a qualified architect review outputs and make final architecture decisions before implementation. <br>


## Reference(s): <br>
- [SA Master ClawHub listing](https://clawhub.ai/leo21cn/sa-master) <br>
- [SA Master MCP service endpoint](https://mcp.smartmoves.com.cn/sa/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance, with generated architecture documents, review reports, Mermaid diagrams, and shell commands for remote MCP tool calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote MCP service for architecture-design workflows; outputs should be reviewed by a qualified architect before use.] <br>

## Skill Version(s): <br>
1.5.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
