## Description:

Creates weekly shift rosters (KW-JSON) from CSV availability data and pushes them to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT-0

## Use Case:

Field sales coordinators and operations staff use this skill to create weekly shift rosters from CSV availability data, validate staffing constraints, and publish roster JSON for PDF or email workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify GitHub-backed employee records and roster files.

Mitigation: Use a private target repository, restrict GITHUB_TOKEN to the single repository with only required permissions, and require manual diff approval before employees.json or roster changes are committed.

Risk: The skill triggers GitHub Actions workflows that may build PDFs, send Telegram messages, or send employee emails.

Mitigation: Review build-roster.yml and publish-roster.yml before installation and confirm they only perform intended PDF generation and delivery actions.

Risk: Inline JSON shell arguments can be unsafe or fragile for generated roster and employee data.

Mitigation: Pass JSON to scripts through files or stdin instead of documented inline JSON command arguments.

Risk: Employee names, email addresses, minor status, hour limits, notes, and weekly assignments are personal data.

Mitigation: Store only necessary roster data, keep the repository private, and apply applicable data protection requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kleberbaum/skills/roster)
- [ClawHub Publisher Profile](https://clawhub.ai/user/kleberbaum)
- [README](artifact/README.md)
- [Basic Usage Example](artifact/examples/basic.md)
- [Command Examples](artifact/examples/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON roster content and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITHUB_TOKEN, ROSTER_REPO, curl, python3, base64, Linux, and a GitHub repository with roster workflows.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
