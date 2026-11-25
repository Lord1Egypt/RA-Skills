## Description:

Package a Python (especially Tkinter / GUI) script into a single-file Windows .exe that launches by double-click with no console window.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to package Python applications, especially Tkinter desktop tools, as Windows executables. It provides local build commands, troubleshooting guidance, and optional GitHub Actions release configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags potentially disruptive Explorer repair or file overwrites, and analysis coverage is partial.

Mitigation: Review the Explorer repair and Desktop copy steps before running them; keep a backup of icon-cache files and confirm destination paths and existing files before copying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oracis/skills/pyinstaller-pack-windows)
- [build-exe-cmd.md](references/build-exe-cmd.md)
- [gotchas.md](references/gotchas.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python, batch, PowerShell, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples are adapted to the user's app and Windows build setup.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
