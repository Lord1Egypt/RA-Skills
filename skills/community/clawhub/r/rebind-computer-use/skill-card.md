## Description:

Drive this computer with a real hardware keyboard and mouse via Rebind: click, type, browse, fill forms, and operate desktop GUIs, including apps that reject synthetic input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usinput](https://clawhub.ai/user/usinput)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate Windows or macOS desktop applications through Rebind-controlled hardware or software input. It is intended for GUI tasks such as browsing, form entry, desktop app operation, and visual checkpoint verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad computer-control capabilities through a Rebind MCP integration.

Mitigation: Run from a low-privilege account or sandbox where possible, and require explicit user confirmation before actions that send data, change accounts, delete content, post publicly, or make purchases.

Risk: The MCP server package is installed through an unpinned remote package reference.

Mitigation: Install only if the Rebind service and @rebind.gg MCP package publisher are trusted, and review or pin the MCP server version before use.

Risk: Desktop control can expose sensitive files, clipboard contents, credentials, or environment variables.

Mitigation: Avoid exposing sensitive local data to the controlled session and do not enter credentials, payment details, or 2FA codes unless they were supplied for the exact task.

Risk: GUI automation can mis-click or act on the wrong window if visual state is stale or mouse calibration is off.

Mitigation: Use checkpoint verification with screenshots, zoomed regions, or script return values, and recalibrate or stop after repeated failed verifications.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/usinput/skills/rebind-computer-use)
- [Rebind Homepage](https://rebind.gg)
- [Rebind Download](https://rebind.gg/download)
- [@rebind.gg/mcp-server](https://www.npmjs.com/package/@rebind.gg/mcp-server)
- [README.md](README.md)
- [mcp.example.json](mcp.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Text]

**Output Format:** [Markdown with inline shell, JSON, and Luau code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bun, a Rebind relay URL in REBIND_URL, and the @rebind.gg/mcp-server package; supports Windows and macOS.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
