## Description:

Read and modify Quire tasks, projects, comments, statuses, and tags via the quire CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quire](https://clawhub.ai/user/quire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent inspect Quire workspaces, summarize tasks and projects, and perform confirmed task updates through the local Quire CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use the logged-in Quire CLI account to read and modify Quire data.

Mitigation: Require explicit user confirmation before create, update, complete, uncomplete, date, or comment actions.

Risk: The comment feature can send arbitrary local file contents to Quire via @/path/to/file.

Mitigation: Avoid approving file-backed comments unless the full file contents and destination task are shown first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quire/skills/quire)
- [Quire](https://quire.io)
- [Quire CLI](https://github.com/quire-io/quire-cli)
- [Quire API documentation](https://quire.io/dev/api/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the quire CLI on PATH and an existing quire login session.]

## Skill Version(s):

0.3.1 (source: frontmatter, release metadata, changelog released 2026-05-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
