## Description:

Manually change a task node in the TODO.md tree. Use for /todo-update <ID> [--status in-progress|blocked|ready|drop|revert] [--note "<message>"], where ID may be dotted like FEAT-002.1. Changes markers, drops a node with its subtree after confirmation, and edits Title, Done when, Ref, Depends, From, State, Complexity, Priority or Lane in place using only text the user supplied.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bassemzohdy](https://clawhub.ai/user/bassemzohdy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect or update a task in a TODO.md tree, including its status or user-supplied fields. It applies the tree's dependency, branch, and confirmation rules while making the requested backlog change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A blocked-task update may commit implementation changes along with a backlog update.

Mitigation: Review the changed and staged paths before accepting the commit, and confirm that its scope is appropriate.

Risk: The available security assessment has medium confidence and incomplete checks.

Mitigation: Review the skill's proposed changes before use, especially when a status action may create or alter a commit.

## Reference(s):

- [Source repository (todo-update)](https://github.com/bassemZohdy/todo-skills/tree/main/plugin/skills/todo-update)
- [ClawHub skill page](https://clawhub.ai/bassemzohdy/skills/todo-update)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [TODO.md changes with concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Changes are limited to the requested task fields and tree markers; dropping a task subtree requires confirmation.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
