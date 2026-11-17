## Description:

Manage tasks, todos and reminders using the todo.txt CLI (todo.sh). Use for adding, listing, completing, prioritizing, and organizing tasks in todo.txt format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eaguilera23](https://clawhub.ai/user/eaguilera23)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage a portable todo.txt task list conversationally through todo.sh, including adding, listing, filtering, prioritizing, editing, completing, archiving, and deleting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install todo.sh from the internet and may use elevated privileges on Linux if todo.sh is missing.

Mitigation: Install todo.sh yourself from a trusted, pinned source before enabling the skill, and do not allow an agent to run the installer automatically.

Risk: Task edit, delete, archive, deduplicate, move, and force-flag commands can alter local todo.txt files.

Mitigation: Require confirmation for destructive or force-flag operations and test with a throwaway todo.txt file when evaluating the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eaguilera23/skills/todo-txt-skill)
- [todo.txt CLI](https://github.com/todotxt/todo.txt-cli)
- [todo.txt format](https://github.com/todotxt/todo.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and todo.txt task text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local todo.txt task files and may invoke an installer if todo.sh is missing.]

## Skill Version(s):

1.0.0 (source: server release metadata; changelog released 2026-06-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
