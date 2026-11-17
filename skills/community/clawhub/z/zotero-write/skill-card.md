## Description:

Write, tag, annotate, and edit a local Zotero SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyononthemoon](https://clawhub.ai/user/lyononthemoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Zotero users use this skill to add tags and notes, update bibliographic metadata, inspect item fields, and create new entries in a local Zotero SQLite database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directly changes a local Zotero SQLite database, which can corrupt or overwrite important library data if used incorrectly.

Mitigation: Use it only for explicit Zotero write requests, close Zotero before writing, and keep an independent backup of the actual zotero.sqlite file.

Risk: The backup safeguard can be bypassed by passing mismatched --db and --backup paths.

Mitigation: Verify that --db and --backup refer to the same database before executing write operations, and avoid custom path combinations unless they have been checked.

Risk: Updating a metadata field replaces any existing value for that field.

Mitigation: Inspect item details before editing and confirm the target item key, field name, and replacement value before running a write command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyononthemoon/skills/zotero-write)
- [ClawHub publisher profile](https://clawhub.ai/user/lyononthemoon)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell commands and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and command invocations for local Zotero database write operations; the bundled script prints operation status, backup paths, item keys, and errors.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
