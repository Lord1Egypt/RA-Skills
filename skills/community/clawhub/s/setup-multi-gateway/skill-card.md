## Description:

Configures and runs multiple independent OpenClaw gateway instances with separate agents, workspaces, ports, and optional Feishu bot identities for multi-agent collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create isolated OpenClaw gateway instances for separate agents, workspaces, and bot identities. It supports multi-agent task distribution and autonomous status reporting through Feishu when that channel is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe credential handling can expose API keys, model configuration secrets, or Feishu application secrets.

Mitigation: Treat generated model and Feishu configuration files as secret-bearing files, restrict local access, and rotate any embedded API key before use.

Risk: The wizard creates long-running user systemd services from supplied gateway settings.

Mitigation: Run it only on machines where persistent OpenClaw gateway services are expected, then review generated service files before enabling or starting them.

Risk: Unvalidated gateway names and suggested values can affect generated paths, service names, tokens, and configuration values.

Mitigation: Use a fixed gateway name containing only letters, numbers, underscores, or hyphens, and do not accept values from untrusted sources.

Risk: Broad Feishu permissions can grant more access than a deployment needs.

Mitigation: Grant only the Feishu scopes required for the intended bot workflow and avoid importing broad permission bundles by default.

## Reference(s):

- [Setup Multi Gateway on ClawHub](https://clawhub.ai/pikaqiuyaya/skills/setup-multi-gateway)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [feishu-agent-send skill](https://clawhub.com/skills/feishu-agent-send)
- [ClawHub skill marketplace](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and an interactive Node.js setup wizard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-facing setup steps and may create OpenClaw configuration files, workspace directories, Feishu channel settings, and user systemd service files when the wizard is executed.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
