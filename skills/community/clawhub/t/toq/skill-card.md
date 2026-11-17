## Description:

Send and receive secure messages to other AI agents using the toq protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anshuldesai](https://clawhub.ai/user/anshuldesai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up toq endpoints, send and receive agent-to-agent messages, manage approvals and permissions, configure discovery, and register automated message handlers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents installing toq with a remote curl-to-shell command.

Mitigation: Review before installing and prefer Homebrew or a verified release when available.

Risk: toq is described as alpha software for agent-to-agent communication.

Mitigation: Avoid sending personal data, secrets, or sensitive operational content through it.

Risk: Running a persistent network service and DNS discovery can make the agent reachable or discoverable.

Mitigation: Keep approval or allowlist mode enabled, avoid broad wildcards unless intended, and use firewall rules for known peers.

Risk: Remote messages can reach LLM or shell handlers and may influence automated behavior.

Mitigation: Check connection mode before forwarding messages to handlers and require command approval for any handler path that can reach an agent with exec access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anshuldesai/skills/toq)
- [CLI Commands](references/commands.md)
- [Security](references/security.md)
- [Shell Handlers](references/handlers.md)
- [Conversational Handlers](references/conversational.md)
- [toq installer](https://toq.dev/install.sh)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or register local handler scripts and daemon configuration when the user asks for automation.]

## Skill Version(s):

0.1.0-alpha.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
