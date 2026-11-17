## Description:

Production development workflow with TODO tracking, Graphite PRs, GitHub issues, Vercel deploy checks, and SMS notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelmonetized](https://clawhub.ai/user/michaelmonetized)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to follow an opinionated production workflow for implementation tasks, bug fixes, PR creation, review follow-up, deployment checks, and completion reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can stage broad repository changes and publish PRs, issues, and deployment logs without enough scoping or user confirmation.

Mitigation: Narrow when it activates, require confirmation before git, Graphite, GitHub, or deployment actions, stage only task-specific files, and redact logs before creating issues.

## Reference(s):

- [Graphite CLI](https://graphite.dev)
- [GitHub CLI](https://cli.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository file updates, branch names, PR or issue commands, deployment checks, and completion summaries.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
