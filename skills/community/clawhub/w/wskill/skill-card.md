## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaowl1023](https://clawhub.ai/user/zhaowl1023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate web pages through agent-browser commands for navigation, UI interaction, form filling, screenshots, PDF export, recording, state management, and structured data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookies, localStorage, request headers, saved browser state, and captured network data can expose sensitive account or session information.

Mitigation: Install from a trusted, pinned release when possible; protect and delete saved auth state like a password; avoid printing or sharing cookies, storage, headers, and captured network data.

Risk: Browser automation can perform unintended actions on live websites if commands target the wrong page, session, or element.

Mitigation: Inspect snapshots before interaction, confirm URLs and element references after navigation, and test workflows with non-sensitive sessions before using authenticated accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaowl1023/skills/wskill)
- [agent-browser project](https://github.com/vercel-labs/agent-browser)
- [Agent-Browser-CLI issue tracker](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include JSON-output options for commands that support machine-readable responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
