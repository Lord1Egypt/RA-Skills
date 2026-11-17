## Description:

TunnelProxy lets cloud agents connect to a user's TunnelProxy service for remote command execution, file transfer, and HTTP proxying through the user's machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turinfohlen](https://clawhub.ai/user/turinfohlen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use TunnelProxy when an agent sandbox lacks network access, local tools, or file transfer and they intentionally want the agent to operate through a local TunnelProxy service. Use should be limited to controlled environments where the user accepts remote-execution risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud agents can receive broad command and file access to the user's computer.

Mitigation: Install only in an isolated disposable VM or container under a dedicated low-privilege account without sensitive files, credentials, browser sessions, or internal-network access.

Risk: Public exposure can make remote execution and file transfer reachable beyond the intended agent.

Mitigation: Do not expose it publicly unless you add TLS, authentication, allowlists, logging, and per-action approval controls; prefer binding to 127.0.0.1 when possible.

Risk: Agent output may propose destructive, unauthorized, or privacy-invasive commands.

Mitigation: Require user approval for commands, prefer read-only actions, inspect logs, and refuse actions outside the user's explicit authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turinfohlen/skills/tunnel-proxy)
- [TunnelProxy project homepage](https://github.com/TurinFohlen/tunnel_proxy)
- [TunnelProxy package](https://hex.pm/packages/tunnel_proxy)
- [Protocol reference](references/protocol.md)
- [Agent safety guidance](references/README_for_agent.md)
- [User guidance](references/README_for_user.md)
- [Practical tips](references/TIPS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python snippets, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands and file-transfer guidance that operate through a user-supplied TunnelProxy endpoint.]

## Skill Version(s):

1.0.11 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
