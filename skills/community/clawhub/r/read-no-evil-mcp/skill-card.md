## Description: <br>
Secure email access via read-no-evil-mcp. Protects against prompt injection attacks in emails. Use for reading, sending, deleting, and moving emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thekie](https://clawhub.ai/user/thekie) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent list, read, send, move, and delete email through a read-no-evil-mcp server that scans messages for prompt injection before content reaches the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to send, move, or delete email. <br>
Mitigation: Use read-only or tightly scoped account permissions where possible and require explicit user approval before any send, move, or delete action. <br>
Risk: Email accounts and folders may expose sensitive content to an agent. <br>
Mitigation: Configure only accounts and folders the user is comfortable exposing, and prefer restricted credentials for agent access. <br>
Risk: Remote HTTP server connections can expose email traffic if used outside localhost. <br>
Mitigation: Use HTTPS for non-localhost server connections, as the skill documentation recommends. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thekie/read-no-evil-mcp) <br>
- [read-no-evil-mcp server](https://github.com/thekie/read-no-evil-mcp) <br>
- [ProtectAI DeBERTa prompt-injection model](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Email content and actions are mediated by a configured read-no-evil-mcp server.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata and changelog, released 2026-02-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
