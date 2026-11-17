## Description:

Load x-cmd in a POSIX shell so an agent can discover x-cmd skills and install or use portable development tools through x-cmd and pixi commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwinjhlee](https://clawhub.ai/user/edwinjhlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to load x-cmd, browse available x-cmd skills, and run commands that install or expose portable software such as jq, Node.js, Python, and other development tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an agent-usable remote installer path that can execute mutable downloaded shell code before independent verification.

Mitigation: Prefer Homebrew installation or a manual download-and-review flow; avoid the auto-install path on machines with secrets.

Risk: An agent could install x-cmd or packages without the user's explicit intent.

Mitigation: Do not let an agent install x-cmd or packages unless the user explicitly requested that action and trusts the package sources.

## Reference(s):

- [x-cmd ClawHub Skill Page](https://clawhub.ai/edwinjhlee/skills/x-cmd)
- [x-cmd Website](https://www.x-cmd.com)
- [x-cmd LLMs Reference](https://www.x-cmd.com/llms.txt)
- [x-cmd Repository](https://github.com/x-cmd-skill/x-cmd)
- [Installation Guide](data/install.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may download and install user-local tools after explicit user consent.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
