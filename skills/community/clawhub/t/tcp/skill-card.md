## Description:

Helps with TCP sockets, client/server connections, and network debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to write TCP client or server examples, test port connectivity, debug connection failures, and reason about raw TCP protocol behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated network test commands can perform real network activity against hosts and ports.

Mitigation: Run generated commands only against systems and networks where the user has permission.

Risk: Generated TCP server examples can expose a listening service if bound to public interfaces.

Mitigation: Use loopback addresses for local testing and add authentication, rate limiting, and firewall controls before exposing services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills/tcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated commands and examples may need OS, shell, host, port, and permission context before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
