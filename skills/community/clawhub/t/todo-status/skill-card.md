## Description:

Read-only view of the TODO.md task tree. Use for /todo-status [--search <text>] [--last <N>]. Shows the tree with markers and complexity, progress bars per root, per lane and overall, the active node, the next workable node, blocked nodes with their reasons, and recently drained work from CHANGELOG.md. Searches TODO.md and CHANGELOG.md. Never changes any file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bassemzohdy](https://clawhub.ai/user/bassemzohdy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect TODO.md progress and task priorities, identify active or blocked work, review recent CHANGELOG.md entries, or search these files without changing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had medium confidence because two referenced local paths were unavailable, so their contents were not assessed.

Mitigation: Check that the skill's referenced local materials are available and review them before relying on the resulting status report.

## Reference(s):

- [Source repository](https://github.com/bassemZohdy/todo-skills/tree/main/plugin/skills/todo-status)
- [ClawHub release](https://clawhub.ai/bassemzohdy/skills/todo-status)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Concise Markdown status report or text search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only snapshot of TODO.md and CHANGELOG.md contents at the time of use.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
