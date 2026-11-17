## Description:

Turns a work request into scoped TODO.md tasks with complexity ratings and runnable completion checks, then adds them to the task tree without starting the work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bassemzohdy](https://clawhub.ai/user/bassemzohdy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use /todo-add to turn a work request into a prioritized, complexity-rated task tree with explicit completion checks in TODO.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A single task may be added without a separate confirmation, even when its scope or details need review.

Mitigation: Review the proposed task and its completion check when your workflow requires approval before backlog changes.

Risk: Some referenced local paths may be unavailable, leaving the skill's supporting guidance incomplete.

Mitigation: Ensure the TODO core skill and referenced verification guidance are available before relying on their rules.

## Reference(s):

- [ClawHub todo-add release](https://clawhub.ai/bassemzohdy/skills/todo-add)
- [GitHub source (plugin/skills/todo-add)](https://github.com/bassemZohdy/todo-skills/tree/main/plugin/skills/todo-add)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [TODO.md task tree entries with inline completion command text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adds tasks to TODO.md; does not start the work.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
