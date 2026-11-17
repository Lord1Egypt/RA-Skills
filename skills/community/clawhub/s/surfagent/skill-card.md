## Description:

Control a real Chrome browser via SurfAgent to navigate, click, type, screenshot, extract data, crawl sites, and automate web workflows using a persistent local Chrome profile through SurfAgent's MCP server or direct HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentossoftware](https://clawhub.ai/user/agentossoftware)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to operate a local Chrome browser for web navigation, form interaction, screenshots, structured extraction, crawling, and tab management when persistent browser sessions are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SurfAgent can give external components broad control over a real logged-in Chrome profile.

Mitigation: Use a dedicated Chrome profile or low-privilege accounts, and avoid sensitive sites unless the automation task requires them.

Risk: Browser automation can submit forms, edit cookies, change settings, send messages, or complete purchases.

Mitigation: Require explicit confirmation before purchases, messages, settings changes, cookie edits, or form submissions.

Risk: The skill depends on the SurfAgent desktop app and MCP server packages.

Mitigation: Verify the desktop app source and pin reviewed package versions where possible.

## Reference(s):

- [SurfAgent](https://surfagent.app)
- [SurfAgent MCP Server](https://github.com/surfagentapp/surfagent-mcp)
- [SurfAgent Documentation](https://github.com/surfagentapp/surfagent-docs)
- [ClawHub SurfAgent Skill](https://clawhub.ai/agentossoftware/skills/surfagent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown, JSON]

**Output Format:** [Markdown instructions with inline shell commands and JSON or markdown data returned by browser extraction tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce browser screenshots through the SurfAgent browser_screenshot tool.]

## Skill Version(s):

1.0.0 (source: target metadata, release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
