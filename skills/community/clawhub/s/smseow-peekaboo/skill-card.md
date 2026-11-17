## Description:

Smseow Peekaboo helps an agent view and control a desktop on macOS, Linux, or WSL2 using Peekaboo, MCP desktop tools, or X11 automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect the screen, take screenshots, click, type, and send hotkeys across macOS, Linux, or WSL2 desktop environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent view the desktop and automate clicks, typing, and hotkeys.

Mitigation: Use it only when desktop control is intentional, avoid passwords and sensitive sessions, grant screen or accessibility permissions only after review, and revoke permissions when finished.

Risk: The setup guidance includes unpinned third-party packages and repositories.

Mitigation: Pin and verify package or repository versions before running the commands.

## Reference(s):

- [kwin-mcp](https://github.com/bhyoo/kwin-mcp)
- [VcXsrv](https://github.com/ArcticaProject/vcxsrv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose desktop-control commands that can view the screen, click, type, and use hotkeys.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
