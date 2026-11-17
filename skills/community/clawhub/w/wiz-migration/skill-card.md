## Description:

Helps migrate WizNote data by detecting local storage directories, guiding HTML export, and copying exported attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awamwang](https://clawhub.ai/user/awamwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and note-system users use this skill to plan a WizNote export, generate migration guidance, and move attachment folders into a target note archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that an optional Windows batch-script path can execute arbitrary local commands if an unreviewed script_path is supplied.

Mitigation: Use the pure-Python migration path with source and target directories chosen by the user, and pass script_path only after reviewing the batch file.

Risk: Migration helpers may write local paths or notes to migration_log.json.

Mitigation: Review generated logs before sharing them outside the local migration environment.

Risk: File migration can fail or copy incomplete data if the wrong source or export directory is selected.

Mitigation: Back up the original WizNote data and validate the exported HTML and attachment folders before and after migration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/awamwang/skills/wiz-migration)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional generated migration log JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate wiz_export_guide.md and migration_log.json when invoked by an agent or local workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
