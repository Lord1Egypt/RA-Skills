## Description:

This skill helps agents discover, search, modify, validate, and import Unreal Engine DataTable JSON for AI Skills configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mufuxiao515-create](https://clawhub.ai/user/mufuxiao515-create)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical content teams use this skill to inspect and edit Unreal Engine AI Skills DataTable JSON, validate changes, and generate UE Editor import commands for updating DataTable assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly scan local directories for Unreal projects and DataTable JSON files.

Mitigation: Prefer explicit project roots and JSON paths to limit discovery scope.

Risk: The skill can make persistent changes to DataTable JSON and UE assets.

Mitigation: Use dry-run first, keep source-control backups, and review generated UE commands before running them.

Risk: The built-in validator is not a hard safety gate for every bad DataTable edit.

Mitigation: Review modified rows and UE import logs before treating changes as final.

## Reference(s):

- [README](README.md)
- [AI Skills JSON Field Schema](references/field_schema.md)
- [ClawHub Skill Page](https://clawhub.ai/mufuxiao515-create/skills/ue-datatable-editor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run previews, validation summaries, backup notices, and UE Editor import commands.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
