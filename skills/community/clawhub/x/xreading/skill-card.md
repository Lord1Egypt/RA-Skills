## Description:

XReading helps an agent turn a book title or local PDF/EPUB into a concise Chinese reading card with a gate decision, core argument chain, actionable rules, quick red-flag checks, and workspace index updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutd](https://clawhub.ai/user/cutd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process books into reusable Chinese Markdown notes, decide whether a book merits deeper reading, extract practical rules, and keep lightweight reading and usage indexes current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may search local Downloads or Books folders and may use online lookup when the user gives only a book name.

Mitigation: Provide an explicit file path and ask the agent not to search local folders or go online when book interests or local file names should remain private.

Risk: Generated notes can include sensitive personal context, investment interests, or holdings when the book analysis is applied to real decisions.

Mitigation: Review generated Markdown before syncing or publishing, and keep reading-derived ideas separate from any independent investment decision process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cutd/skills/xreading)
- [Card Template](artifact/references/card-template.md)
- [Project Context](artifact/references/project-context.md)
- [Quality Rules](artifact/references/quality-rules.md)
- [Workspace Files](artifact/references/workspace-files.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown files with brief chat summaries and occasional shell commands for quality checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update book cards, verification notes, reading lists, and candidate-rule logs in the user's workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
