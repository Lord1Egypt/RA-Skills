## Description:

AI-powered parametric furniture modeling for Fusion 360 that generates production-ready CAD models with real joinery from natural language, images, or reference links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylzha](https://clawhub.ai/user/ylzha)

### License/Terms of Use:

MIT

## Use Case:

External developers, CAD users, and furniture designers use Shopprentice to turn natural-language, image, or reference-link furniture requests into parametric Fusion 360 Python scripts, live MCP-driven builds, validation steps, and iterative design guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and exposes local execution paths that can run generated Python and modify Fusion 360 CAD documents.

Mitigation: Run it only in a trusted local environment, review generated scripts before execution when possible, and keep valuable Fusion documents backed up.

Risk: The documented one-line installer uses a remote shell command.

Mitigation: Prefer cloning or downloading a pinned release and inspecting the installer before running it.

Risk: The Fusion 360 MCP add-in exposes powerful local actions over a localhost JSON-RPC server.

Mitigation: Keep the service local-only, run it only when needed, and avoid bypassing agent sandbox protections unless the local-system access is understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylzha/skills/shopprentice)
- [Project homepage](https://github.com/ShopPrentice/shopprentice)
- [MCP Integration for Fusion 360](artifact/mcp/README.md)
- [Joinery Reference](artifact/docs/joinery/README.md)
- [Fusion 360 API Rules](artifact/docs/fusion-api-rules.md)
- [Organic Shapes](artifact/docs/organic-shapes.md)
- [Hardware Installation](artifact/docs/hardware-installation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets, generated Fusion 360 Python scripts, and local configuration details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute generated scripts through a local Fusion 360 MCP add-in when configured; scripts can also be reviewed and run manually.]

## Skill Version(s):

0.7.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
