## Description:

A Chinese-language personal todo manager that tracks pending, in-progress, and completed tasks with optional GitHub issue and path associations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangruilin](https://clawhub.ai/user/tangruilin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage personal workspace todos conversationally, including creating, querying, starting, completing, deleting, and tracking task metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task data is stored in workspace JSON files and may include local paths or private issue links.

Mitigation: Avoid recording sensitive local paths or private issue URLs unless workspace storage is acceptable.

Risk: Fuzzy matching and immediate deletion or status changes can affect the wrong todo.

Mitigation: Use precise task names or IDs before delete and status changes.

## Reference(s):

- [Data schema](references/data-schema.md)
- [Usage examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/tangruilin/skills/todo-manage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown conversational responses and local JSON todo files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores todos_pending.json, todos_in_progress.json, todos_completed.json, and todos_meta.json in the workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
