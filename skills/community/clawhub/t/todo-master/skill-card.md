## Description:

待办大师 helps agents manage local todos through a Python CLI backed by a user-confirmed SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asir-zhang](https://clawhub.ai/user/asir-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to keep local task lists, query due work, and update task status without relying on an online service. It is suited to single-user local workflows that need a CLI and durable SQLite storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a local configuration file and SQLite todo database.

Mitigation: Initialize it only after confirming the intended storage directory, and use an existing absolute path when choosing custom storage.

Risk: Reference documents describe an older file-partitioned design while the current SKILL.md and script use SQLite.

Mitigation: Use SKILL.md and scripts/todo.py as the operational source for current commands and storage behavior.

## Reference(s):

- [OpenClaw Todo Skill Introduction](references/INTRO.md)
- [OpenClaw Todo Skill Technical Design (V1)](references/TECH_SPEC.md)
- [ClawHub Skill Page](https://clawhub.ai/asir-zhang/skills/todo-master)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Configuration]

**Output Format:** [Human-readable CLI text or JSON, with local config and SQLite data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates config.json and a local SQLite todo database in the user-confirmed data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
