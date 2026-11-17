## Description:

Uses Chrome DevTools via MCP for efficient debugging, troubleshooting and browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-din](https://clawhub.ai/user/a-din)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, debug, and automate browser pages through Chrome DevTools MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime setup automatically runs an unpinned npm package.

Mitigation: Prefer a release that pins chrome-devtools-mcp to a reviewed exact version before installation.

Risk: Chrome is launched with sandbox protections disabled.

Mitigation: Run the skill only inside a dedicated low-privilege container or VM with a temporary browser profile and no sensitive logged-in sessions.

## Reference(s):

- [Chrome DevTools documentation](https://developer.chrome.com/docs/devtools)
- [Chrome DevTools AI assistance documentation](https://developer.chrome.com/docs/devtools/ai-assistance)
- [Chrome DevTools MCP troubleshooting](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/a-din/skills/xiaopi-chrome-devtools)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and MCP workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference generated browser artifacts such as screenshots, snapshots, and traces when the MCP server is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
