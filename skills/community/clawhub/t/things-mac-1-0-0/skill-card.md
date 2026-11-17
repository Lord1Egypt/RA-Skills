## Description:

Manage Things 3 via the `things` CLI on macOS, including adding or updating projects and todos through the URL scheme and reading, searching, or listing local Things database content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent manage Things 3 tasks, projects, areas, tags, and scheduling details on macOS through the `things` command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party `things3-cli` project.

Mitigation: Install only if the upstream project is trusted, and consider reviewing or pinning the exact version before installing.

Risk: Local Things database reads may require Full Disk Access.

Mitigation: Grant Full Disk Access only to the minimum calling application needed for the workflow.

Risk: `THINGS_AUTH_TOKEN` enables update operations.

Mitigation: Treat `THINGS_AUTH_TOKEN` as a secret and avoid exposing it in logs, transcripts, or shared configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenswj/skills/things-mac-1-0-0)
- [things3-cli GitHub Repository](https://github.com/ossianhempel/things3-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; requires the `things` binary and may need Full Disk Access or `THINGS_AUTH_TOKEN` for specific operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
