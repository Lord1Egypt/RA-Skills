## Description: <br>
Desktop-control guidance for agents using Peekaboo on macOS and MCP or X11-based tools on Linux and WSL2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or supervised users who intentionally want an agent to inspect and operate a desktop use this skill for screenshot, click, typing, hotkey, and app-control workflows across macOS, Linux, and WSL2. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill gives an agent broad screen, mouse, keyboard, and app-control authority. <br>
Mitigation: Install only for intentional desktop-control use, keep sessions supervised, and require explicit confirmation before screenshots, typing, clicks, hotkeys, app launches, deletions, account changes, payments, or security and privacy prompts. <br>
Risk: The skill relies on external desktop-control tools and OS permissions. <br>
Mitigation: Review the external tools and install commands before use, grant only the required OS permissions, and run in an environment where unintended desktop actions can be safely interrupted. <br>


## Reference(s): <br>
- [kwin-mcp](https://github.com/bhyoo/kwin-mcp) <br>
- [VcXsrv](https://github.com/ArcticaProject/vcxsrv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require local tool installation and OS-level desktop-control permissions.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
