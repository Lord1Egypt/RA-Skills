## Description:

Super Product is a task-management CLI guide for managing Super Productivity tasks, counters, projects, and daily status from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and task-management users use this skill to operate the Super Productivity CLI for listing, searching, creating, editing, completing, and deleting tasks and counters, and for viewing projects and daily status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides installation of an unpinned Python package that runs on the user's machine.

Mitigation: Install the package in a virtual environment, verify the package source before use, and review package updates before upgrading.

Risk: The documented edit, completion, logging, and delete commands can modify Super Productivity task-management data.

Mitigation: Use list or search commands to confirm IDs first, keep recoverable backups or sync history, and review command arguments before running data-changing operations.

Risk: Windows users may encounter the compatibility and encoding issues documented by the artifact.

Mitigation: Use JSON output or set PYTHONIOENCODING=utf-8 for encoding issues, and verify runtime compatibility before depending on the CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/super-product)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI output-format guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents JSON, NDJSON, and full entity output options for the external CLI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
