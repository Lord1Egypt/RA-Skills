## Description:

Connect Hermes Agent to Zed via the Agent Client Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers using Linux and Zed use this skill to connect Hermes Agent as an ACP External Agent, configure Zed agent_servers, and troubleshoot launch, credential, permission, Flatpak, and MCP boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsandboxed or broadly approved External Agent tool use could allow Hermes actions beyond the user's intended scope.

Mitigation: Keep tool permissions on confirm or narrowly scoped allow rules, and avoid global auto-approve for the Hermes External Agent.

Risk: Users may assume Zed manages Hermes credentials, tools, MCP configuration, or provider data handling.

Mitigation: Verify Hermes credentials, MCP configuration, and provider data policies separately from Zed's native agent settings.

Risk: Incorrect Zed settings edits, especially for Flatpak JSONC files or sandbox command paths, can prevent Zed from launching Hermes.

Mitigation: Review changes before saving, preserve JSONC syntax where applicable, and use the documented in-sandbox Hermes command path for Flatpak installs.

## Reference(s):

- [Project homepage](https://github.com/mina-atef-00/agent-skills)
- [Zed External Agents (ACP)](references/zed-external-agents.md)
- [Wiring Hermes into the Zed Flatpak](references/zed-flatpak-setup.md)
- [Zed Agent Paths](references/zed-agent-paths.md)
- [Zed Agent UI Reference](references/zed-agent-ui.md)
- [Zed Tools, Permissions & Sandboxing](references/zed-tools-permissions.md)
- [Zed Skills, MCP & Instructions](references/zed-mcp-skills-instructions.md)
- [Zed AI Features](references/zed-ai-features.md)
- [Zed AI Privacy & the Hermes Boundary](references/zed-ai-privacy.md)
- [Zed CLI Reference](references/zed-cli.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux-focused Zed and Hermes ACP setup guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
