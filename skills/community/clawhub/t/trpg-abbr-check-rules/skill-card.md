## Description:

Use this skill when checking and fixing English abbreviations in TRPG rulebooks, scenarios, character sheets, catalogs, maps, and other player/GM-facing files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to review TRPG rules, scenarios, character sheets, catalogs, and maps for English abbreviations that should be expanded into Traditional Chinese full-name abbreviation style. It helps normalize player- and GM-facing game terminology across Markdown, YAML, spreadsheet, and map-label content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch abbreviation replacement may alter many player- or GM-facing files and introduce incorrect terminology if unchecked.

Mitigation: Review the resulting diffs before committing or publishing, with special attention to repeated term expansions and table-specific abbreviation exceptions.

Risk: The skill intentionally skips obvious backups, drafts, and transitional files, which may omit files a user expected to update.

Mitigation: Confirm the target file set before applying changes when older or draft material is still intended for release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ice26985850/skills/trpg-abbr-check-rules)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, plain text, YAML-style content, and spreadsheet label edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply batch edits across relevant TRPG-facing files while skipping obvious backups, drafts, and superseded transitional files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
