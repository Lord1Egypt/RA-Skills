## Description:

Workday Calendar helps agents manage statutory holidays, makeup workdays, rotating shifts, special rest days, personal schedules, and calendar exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Employees, operators, and scheduling agents use this skill to calculate workdays, maintain holiday and compensatory-workday rules, manage local personal schedules, and export calendar or shift views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web configuration server can expose and change calendar data over a network without authentication.

Mitigation: Run the configuration server only on trusted machines and networks; bind it to 127.0.0.1 and add authentication before broader use.

Risk: Imported rules and generated HTML can carry untrusted values.

Mitigation: Validate holiday and schedule inputs before import, and escape or review generated HTML before sharing or opening it in sensitive environments.

Risk: The skill writes local calendar data and creates executable backup scripts.

Mitigation: Keep backups of the data directory, review generated backup scripts before execution, and restrict write access to the intended local calendar workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/workday-calendar)
- [Guide](artifact/references/guide.md)
- [CLI reference](artifact/references/cli.md)
- [Data format reference](artifact/references/data_format.md)
- [Permissions and security notes](artifact/references/permissions.md)
- [Test report](artifact/references/test-report.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, HTML files]

**Output Format:** [Markdown, JSON, HTML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local calendar JSON data, schedule data, generated HTML exports, and local backup scripts.]

## Skill Version(s):

2.2.0 (source: frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
