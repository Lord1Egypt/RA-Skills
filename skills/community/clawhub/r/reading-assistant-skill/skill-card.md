## Description:

A reading assistant that helps users manage reading excerpts and a personal knowledge base with smart tags, full-text search, bulk import/export, and reading statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, knowledge workers, and agents use this skill to capture book excerpts, organize them by book, chapter, and tag, search prior notes, import Kindle or WeChat Reading exports, and generate reading reports or note exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can read or write outside the intended notes folder when custom paths are used.

Mitigation: Run the skill in a constrained workspace, keep the default reading-notes location where possible, and review any file paths before execution.

Risk: Exported HTML can include unsafe note content.

Mitigation: Avoid opening or sharing HTML exports from untrusted imported notes until HTML escaping and path confinement are fixed; prefer Markdown for untrusted content.

Risk: Imported note files may contain untrusted or malformed content.

Mitigation: Import only trusted note files and review the import preview before saving records.

Risk: Book deletion and bulk import workflows can modify the local reading-notes store.

Mitigation: Require explicit user confirmation for destructive or bulk operations and keep backups of the reading-notes directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ludiansheng/skills/reading-assistant-skill)
- [Data structure definition](references/data-structure.md)
- [Chapter recognition rules](references/chapter-rules.md)
- [Import format specification](references/import-formats.md)
- [Export template guide](references/export-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Agent responses plus JSON note records, JSON search/statistics results, and Markdown or HTML exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local reading-notes JSON files and may write exported Markdown or HTML files.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
