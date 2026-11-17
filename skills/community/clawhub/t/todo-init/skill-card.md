## Description:

Bootstrap and report on the todo backlog workspace. Use for /todo-init [--plan] [--ci] or when the user wants to set up or check TODO.md and CHANGELOG.md. Scans README.md, docs/, TODO.md and CHANGELOG.md, creates the missing backlog files, detects git, runtime, package manager and test command, offers to migrate the old three-section format to the task tree, and reports the tree. Optionally asks pre-planning questions and sets up CI (or a local pre-push fallback) running the backlog lint and the tests. Idempotent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bassemzohdy](https://clawhub.ai/user/bassemzohdy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to initialize or review a project's TODO and changelog files and get a concise report of repository setup. They can also request planning questions or CI setup, with changes made only after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because some referenced paths were absent from the scanned artifact.

Mitigation: Check that the referenced paths are available and expected before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bassemzohdy/skills/todo-init)
- [Source repository path](https://github.com/bassemZohdy/todo-skills/tree/main/plugin/skills/todo-init)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Project setup guidance]

**Output Format:** [Markdown status report, with optional TODO.md, CHANGELOG.md, and CI configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates only missing backlog files; migration and CI setup require user approval.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
