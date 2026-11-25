## Description:

Import and export WordPress posts, pages, comments and media Library data as CSV, XML, JSON, XLSX or ODS through the Import Export plugin Abilities API (rsl-ie/*). Use when the user wants to bulk import a file or feed, export content, map columns, schedule recurring jobs or check why rows failed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dk-wordpress](https://clawhub.ai/user/dk-wordpress)

### License/Terms of Use:

MIT-0

## Use Case:

WordPress site administrators and developers use this skill to guide imports and exports of posts, pages, comments, and media through the Import Export plugin. It helps prepare and validate mappings, review duplicate handling and failed rows, and manage export or recurring job workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Importing with duplicate_mode set to update can overwrite existing WordPress content.

Mitigation: Validate the mapping first, review duplicate handling with the user before starting, and test a small slice of rows for large imports.

Risk: Scheduled jobs and triggers can repeat import or export work.

Mitigation: Use recurring schedules or triggers only when needed, and check the source job and recurrence details before creating them.

Risk: Imported files may contain text that looks like instructions or content the user did not intend to import.

Mitigation: Treat file contents as data and import only content the user requested.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dk-wordpress/skills/wordpress-import-export)
- [Publisher profile](https://clawhub.ai/user/dk-wordpress)

## Skill Output:

**Output Type(s):** [Guidance, API calls]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step WordPress import and export guidance with API request examples and safeguards.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
