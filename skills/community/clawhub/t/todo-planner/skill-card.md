## Description:

Organize todos with priorities, deadlines, weekly views, progress tracking, and exports through a local command-line todo logger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to capture tasks, plan daily or weekly agendas, track progress, review completed work, and search or export local todo records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local task logs and exports may contain sensitive personal or work details in plaintext.

Mitigation: Avoid storing secrets or highly sensitive details, review local file permissions on shared systems, and handle exported files carefully.

Risk: CSV exports can carry spreadsheet-opening risks if todo content is treated as executable formulas.

Mitigation: Review CSV content before opening it in spreadsheet software, especially when entries came from copied or untrusted text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/todo-planner)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Markdown guidance with inline shell commands and local log or export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores plaintext todo logs under ~/.local/share/todo-planner and can export json, csv, or txt files.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
