## Description:

Helps an OpenClaw agent manage Docker containers, marketplace apps, and multi-machine WAGMIOS hosts through scoped API keys, startup checks, and runtime user-provided API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mentholmike](https://clawhub.ai/user/mentholmike)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, homelab operators, and external users use this skill to let an agent inspect and manage Docker containers, images, and marketplace app installs through a WAGMIOS backend. It is especially suited to scoped, multi-host container operations where each host has its own API URL and least-privilege key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct high-impact Docker container actions, including creating, stopping, deleting, and installing applications.

Mitigation: Use least-privilege, per-host API keys, check key scopes before each operation, and require user confirmation for destructive or service-interrupting actions.

Risk: Remote WAGMIOS hosts may expose Docker-management authority if the backend or key is reachable by untrusted parties.

Mitigation: Prefer loopback-only access for local hosts and HTTPS or VPN access for remote hosts; avoid broad docker-group access for general users.

Risk: Container configs, logs, compose files, or bind mounts may expose secrets or sensitive host paths.

Mitigation: Review compose files and bind mounts before starting apps, and do not print container environment values, API keys, or other secret material.

Risk: Bypassing the scoped WAGMIOS API would undermine the intended permission boundary.

Mitigation: Use only the WAGMIOS API for container operations and treat missing scopes or protected-container errors as final until the user changes permissions.

## Reference(s):

- [WAGMIOS ClawHub Listing](https://clawhub.ai/mentholmike/skills/wagmios)
- [API Reference](artifact/references/api.md)
- [Safeguards](artifact/references/safeguards.md)
- [Scope Reference](artifact/references/scopes.md)
- [Workflows](artifact/references/workflows.md)
- [Marketplace Reference](artifact/references/marketplace.md)
- [Docker Installation Guide](artifact/references/docker-install.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples, JSON payloads, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided WAGMIOS base URLs and X-API-Key values at runtime; keys should not be stored or printed.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
