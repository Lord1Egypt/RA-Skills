## Description: <br>
toq protocol helps agents set up, secure, and operate toq-based agent-to-agent messaging, including message sending, connection approvals, DNS discovery, status checks, and handlers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnshulDesai](https://clawhub.ai/user/AnshulDesai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure toq endpoints, exchange messages between agents, manage approvals and permissions, and add shell or LLM handlers for automated workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users through running an alpha network messaging daemon. <br>
Mitigation: Install only when alpha software is acceptable, verify the installer source, avoid sending sensitive data, and prefer approval or allowlist mode. <br>
Risk: Wildcard approvals or overly open connection modes can allow unexpected agents to contact the endpoint. <br>
Mitigation: Use approval or allowlist mode, avoid wildcard approvals unless intentional, and restrict public network exposure where practical. <br>
Risk: Message handlers can run shell commands or forward message contents to LLM providers. <br>
Mitigation: Review handler scripts before registration, check connection mode before forwarding messages, keep exec approval enabled, and enable LLM handlers only when provider exposure is acceptable. <br>


## Reference(s): <br>
- [ClawHub release](https://clawhub.ai/AnshulDesai/toq) <br>
- [toq install script](https://toq.dev/install.sh) <br>
- [CLI Commands](references/commands.md) <br>
- [Conversational Handlers](references/conversational.md) <br>
- [Shell Handlers](references/handlers.md) <br>
- [Security](references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes alpha-use warnings, approval-mode guidance, and handler setup notes.] <br>

## Skill Version(s): <br>
0.1.0-alpha.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
