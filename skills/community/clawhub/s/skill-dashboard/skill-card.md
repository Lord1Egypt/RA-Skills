## Description:

Skill Dashboard helps users view, inspect, update, disable, and uninstall local ClawHub skills through paginated dashboard-style responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[largetool](https://clawhub.ai/user/largetool)

### License/Terms of Use:

MIT

## Use Case:

ClawHub users and skill developers use this skill to review installed skills, inspect marketplace and local usage signals, and manage update, uninstall, enable, or disable actions with confirmation-oriented flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages installed skills through shell-command paths that can be unsafe if skill identifiers are not constrained.

Mitigation: Replace shell-string execution with argument-based command execution and validate skill slugs at every exported entry point.

Risk: Update and uninstall actions can change or remove local skills.

Mitigation: Bind destructive actions to explicit user confirmations and keep confirmation checks close to execution.

Risk: Remote changelog text and marketplace data may be displayed in user-facing output.

Mitigation: Treat remote text as untrusted display data and avoid executing or interpreting it as instructions.

Risk: Local state and cache files influence dashboard behavior.

Mitigation: Constrain state files to fixed local paths and avoid accepting caller-controlled state file locations for broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/largetool/skills/skill-dashboard)
- [Publisher profile](https://clawhub.ai/user/largetool)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown and plain text dashboard reports with inline command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local skill state and cache files when management actions are confirmed.]

## Skill Version(s):

2.0.4 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
