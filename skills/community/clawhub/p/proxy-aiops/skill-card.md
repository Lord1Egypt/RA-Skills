## Description:

Provides governed tools for inspecting Traefik, Caddy, and HAProxy reverse proxies and performing supported proxy configuration or server operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use it to inspect proxy routes, upstream health, certificates, traffic, and configuration, diagnose common availability issues, and perform supported Caddy or HAProxy changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The secrets-store master password could be exposed if saved directly in agent client configuration.

Mitigation: Provide it through a protected runtime secret mechanism instead of storing it in client JSON.

Risk: CLI confirmation prompts do not protect MCP calls, so an agent could make a destructive proxy change.

Mitigation: Start with server-enforced read-only access, require approval in the agent client before enabling writes, and keep an independent configuration backup.

Risk: Audit and undo records may be exposed or unavailable when needed.

Mitigation: Protect audit and undo files, and check audit health before relying on the write history.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zw008/skills/proxy-aiops)
- [Project homepage](https://github.com/AIops-tools/Proxy-AIops)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Configuration guidance]

**Output Format:** [Structured tool results with concise Markdown guidance, plus shell commands or JSON configuration examples when relevant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes proxy health findings and suggested actions; available write operations depend on the target platform.]

## Skill Version(s):

0.13.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
