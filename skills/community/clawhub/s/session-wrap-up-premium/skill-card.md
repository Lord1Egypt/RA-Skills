## Description:

Premium session wrap-up: flush daily log, update MEMORY, update PARA, git commit + push, generate summary. Ensures zero context loss between sessions. Includes customizable templates and optional CI integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neroagent](https://clawhub.ai/user/neroagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to close a work session by preserving notes, updating long-term memory and PARA files, and preparing a Git commit and push. It is intended for users who want repeatable session handoff summaries across agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stage, commit, and push the entire current Git repository.

Mitigation: Review staged files before publishing and disable or remove automatic push unless the repository is ready to publish.

Risk: Unsafe shell command handling could run unintended shell commands.

Mitigation: Replace shell=True Git calls with argument arrays and validate commit messages before execution.

Risk: The skill writes persistent memory and PARA notes.

Mitigation: Review generated notes for sensitive or incorrect content before retaining or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neroagent/skills/session-wrap-up-premium)
- [Publisher profile](https://clawhub.ai/user/neroagent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown reports, JSON summaries, persistent note files, and Git commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write memory and PARA files and may stage, commit, and push repository changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
