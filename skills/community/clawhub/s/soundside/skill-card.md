## Description:

Connects an OpenClaw agent to Soundside MCP tools for AI media generation, editing, library management, and technical analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackthemarket](https://clawhub.ai/user/hackthemarket)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to let an OpenClaw agent generate, edit, analyze, organize, and share media through Soundside's remote MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media, and related project data may be processed by Soundside and its provider backends.

Mitigation: Avoid secrets or regulated data unless the deployment has explicit approval for that data flow.

Risk: Library operations, paid generation, and email-sharing actions can change state, incur cost, or disclose content.

Mitigation: Require explicit user confirmation before delete, update, paid generation, or email-sharing actions.

## Reference(s):

- [Soundside ClawHub Skill Page](https://clawhub.ai/hackthemarket/skills/soundside)
- [Getting Started](https://github.com/soundside-design/soundside-docs/blob/main/guides/getting-started.md)
- [Tool Reference](https://github.com/soundside-design/soundside-docs/blob/main/guides/tools.md)
- [x402 Pay-Per-Call](https://github.com/soundside-design/soundside-docs/blob/main/guides/x402.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and example prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Soundside API key and sends prompts, media, and related project data to Soundside and provider backends.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
