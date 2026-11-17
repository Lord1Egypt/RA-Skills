## Description:

SQLite-based task management with priority, tags, and stats. Database stored in skill directory for natural isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rare](https://clawhub.ai/user/rare)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create, list, inspect, update, complete, archive, delete, and summarize local tasks with priorities, tags, due dates, and status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps a persistent local task database in the skill directory.

Mitigation: Avoid storing sensitive task content unless local persistence is acceptable, and manage the skill data directory according to the workspace retention policy.

Risk: The delete command removes a task record without an extra confirmation prompt.

Mitigation: Inspect the task ID before deleting, or archive tasks when removal is not certain.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rare/skills/task-manager)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Plain text terminal output with persistent SQLite database records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task data under <skill-dir>/data/tasks.db.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
