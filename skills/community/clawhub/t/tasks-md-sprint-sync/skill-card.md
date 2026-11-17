## Description:

Sync TASKS.md current phase and in-progress checklist from the active PLAN.md phase to keep sprint execution aligned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and project maintainers use this skill to compare the active phase in PLAN.md with a project's TASKS.md in-progress list, then optionally update TASKS.md so sprint execution stays aligned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apply mode rewrites the selected project's Current phase and In progress list in TASKS.md.

Mitigation: Run report mode first, set PLAN_FILE and TASKS_FILE to the intended project files, and keep those files under version control before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniellummis/skills/tasks-md-sprint-sync)
- [Publisher profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report mode prints drift without file changes; apply mode updates the selected TASKS.md project section.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
