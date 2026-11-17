## Description:

Set up and diagnose a secure, Nostr-authenticated YunoHost MCP connection in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imattau](https://clawhub.ai/user/imattau)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to configure OpenClaw to connect to a YunoHost MCP endpoint through a local signed bridge, then diagnose enrollment, URL, key-file, and connection issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned setup package can introduce supply-chain risk.

Mitigation: Install only if the yunohost-mcp-connect package and publisher are trusted; for stronger safety, pin or review the package version before setup.

Risk: OpenClaw configuration or generated private keys could be exposed or overwritten during setup or troubleshooting.

Mitigation: Back up the OpenClaw config, use the intended OPENCLAW_CONFIG_PATH, preserve unrelated settings, keep the key file user-readable only, and never share the generated private key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imattau/skills/yunohost-mcp)
- [Project homepage](https://github.com/imattau/yunohost-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uvx and guides the user through OpenClaw configuration, Nostr identity enrollment, and diagnostic checks.]

## Skill Version(s):

0.8.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
