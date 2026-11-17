## Description:

Use when managing QJZD Nav backups, restore, and site settings including uploading background images, logos, and favicons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nqdy666](https://clawhub.ai/user/nqdy666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage QJZD Nav backups, restores, downloads, and site settings through the qjzd-nav CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup delete or import operations can change or remove QJZD Nav site data.

Mitigation: Before delete or import operations, list backups, identify the exact target file, make a fresh export when appropriate, and require explicit confirmation.

Risk: Settings uploads and updates can change site appearance or uploaded assets.

Mitigation: Review the intended file type, setting fields, and target values before running qjzd-nav settings update or upload commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nqdy666/skills/qjzd-nav-cli-operations)
- [qjzd-nav CLI skill](../qjzd-nav-cli)
- [qjzd-nav CLI auth skill](../qjzd-nav-cli-auth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented qjzd-nav commands for automation.]

## Skill Version(s):

1.3.2 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
