## Description:

Guides agents in using Charmbracelet VHS to author, validate, render, and cautiously publish reproducible terminal recordings from .tape files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation authors, and agents use this skill to create deterministic command-line screencasts and documentation assets with Charmbracelet VHS while validating tapes and avoiding secrets, ambient shell state, and unintended publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering a VHS tape can execute commands, modify files, or use the network.

Mitigation: Inspect tapes before rendering, install from trusted sources, and validate syntax before running project commands.

Risk: Terminal recordings can accidentally expose secrets, private paths, customer data, shell history, or account-specific prompts.

Mitigation: Use deterministic sample data and scan tapes and rendered output for sensitive information before committing or sharing.

Risk: VHS publishing uploads output publicly when explicitly requested.

Mitigation: Run publish commands only after the user approves the exact rendered file for public sharing.

## Reference(s):

- [Charmbracelet VHS](https://github.com/charmbracelet/vhs)
- [VHS installation documentation](https://github.com/charmbracelet/vhs#installation)
- [ClawHub skill page](https://clawhub.ai/tmchow/skills/vhs-terminal-recorder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and VHS tape snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce .tape snippets and commands for validation or rendering; public publishing requires explicit user approval.]

## Skill Version(s):

0.1.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
