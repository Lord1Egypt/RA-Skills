## Description:

Science-based habit formation, maintenance, and optimization using behavioral psychology principles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to define, track, troubleshoot, and improve personal habits using behavioral psychology patterns, staged habit formation, and structured markdown logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit logs may include sensitive health, mental-health, location, or routine details.

Mitigation: Keep logs local and private, avoid recording sensitive details unless necessary, and review stored habit files before sharing or syncing them.

Risk: The included tracker script can write outside the intended habit folder when habit names contain slashes, dots, path-like text, or untrusted input.

Mitigation: Use only trusted, simple habit names until path handling is fixed, and review or patch the script before broader installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/self-improving-habit)
- [Habit Definition Template](artifact/assets/HABIT_DEFINITION_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, configuration]

**Output Format:** [Markdown guidance with structured habit log templates and optional shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local markdown habit logs under .learnings/habits when the included tracker script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
