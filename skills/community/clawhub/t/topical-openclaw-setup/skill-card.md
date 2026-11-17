## Description:

Wire Topical into OpenClaw — MCP server, inbound hook transform, and outbound webhook registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daveangelcode](https://clawhub.ai/user/daveangelcode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to connect a Topical account to OpenClaw by configuring the hosted MCP endpoint, installing the inbound hook transform, and registering outbound webhooks in the Topical portal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs and executes companion code that can persist in the OpenClaw gateway path.

Mitigation: Use only a trusted, reviewed, or pinned @daveangelcode/topical companion version and inspect the transform before copying it into ~/.openclaw/hooks/transforms.

Risk: The workflow handles sensitive Agent API keys and hooks.token values.

Mitigation: Do not log, commit, or expose these tokens; keep hooks.token distinct from gateway.auth.token.

Risk: The setup modifies ~/.openclaw/openclaw.json.

Mitigation: Back up ~/.openclaw/openclaw.json before running setup and merge changes without overwriting unrelated configuration.

## Reference(s):

- [Topical](https://usetopical.com)
- [Topical Openclaw Setup on ClawHub](https://clawhub.ai/daveangelcode/skills/topical-openclaw-setup)
- [Companion Topical skill on ClawHub](https://clawhub.ai/daveangelcode/skills/topical)
- [Topical Connect OpenClaw portal](https://app.usetopical.com/portal/openclaw/)
- [Topical hosted MCP endpoint](https://app.usetopical.com/api/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup checks, OpenClaw MCP and hook configuration steps, portal registration guidance, and verification commands.]

## Skill Version(s):

0.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
