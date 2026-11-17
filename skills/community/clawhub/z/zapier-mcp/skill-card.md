## Description:

Connect 8,000+ apps via Zapier MCP. Includes full UI integration for Clawdbot Gateway dashboard. Use when setting up Zapier integration, connecting apps, or using Zapier tools via mcporter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot users use this skill to configure and test a Zapier MCP URL, browse available Zapier actions, and call those tools through mcporter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Zapier MCP URL carries authentication material and is stored in local mcporter configuration.

Mitigation: Treat the URL like a password, restrict dashboard and RPC access, mask it in UI and logs, and regenerate it in Zapier if it is exposed.

Risk: The reference backend accepts user-supplied HTTPS URLs for server-side MCP requests.

Mitigation: Validate saved MCP URLs against the exact Zapier host and expected MCP path before testing, storing, or using them.

Risk: Configured Zapier actions can let an agent affect external services such as messaging, email, spreadsheets, or calendars.

Mitigation: Limit which Zapier actions are exposed to the agent and review high-impact actions before use in shared or sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/zapier-mcp)
- [Zapier MCP](https://zapier.com/mcp)
- [Zapier Help](https://help.zapier.com)
- [Reference README](reference/README.md)
- [Backend Reference](reference/zapier-backend.ts)
- [Controller Reference](reference/zapier-controller.ts)
- [Views Reference](reference/zapier-views.ts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the user's configured Zapier actions and the connected MCP tool schemas.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
