## Description:

Story Writer manages the full fiction-writing process from initial concept through planning, drafting, reviewing, and exporting a formatted book.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahyt77](https://clawhub.ai/user/mahyt77)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to guide a fiction project through discovery, story and book bible planning, chapter drafting, quality review, progress tracking, and HTML export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation commands can create or overwrite local project files, especially when drafting all chapters.

Mitigation: Run the skill in a dedicated project directory and keep backups before broad generation commands.

Risk: Exported HTML may include unsanitized content from discovery data or chapters.

Mitigation: Review or sanitize source content before opening, sharing, or publishing exported HTML.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mahyt77/skills/story-writing-nofuss)
- [Fiction Genres Encyclopedia](references/fiction-genres-encyclopedia.md)
- [Story Structure Frameworks](references/structure-frameworks.md)
- [Revision Checklist](references/revision-checklist.md)
- [World Building Prompts](references/world-building-prompts.md)
- [Query Submission Guide](references/query-submission.md)
- [Writing Style Guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Markdown, and HTML project files plus inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local project files such as discovery.json, story-bible.md, book-bible.md, chapters/*.md, review notes, and export/book.html.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
