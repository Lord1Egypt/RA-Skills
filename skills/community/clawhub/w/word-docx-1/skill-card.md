## Description:

Create, inspect, and edit Microsoft Word documents and DOCX files with reliable styles, numbering, tracked changes, tables, sections, and compatibility checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonydesign1999](https://clawhub.ai/user/tonydesign1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document reviewers, and business users use this skill when an agent needs to create, inspect, or edit Word/DOCX files while preserving styles, numbering, tracked changes, comments, fields, tables, sections, and layout compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Word documents may contain comments, tracked changes, deleted text, or metadata that the user did not intend to expose.

Mitigation: Use the skill only on documents the user is comfortable letting the agent inspect, and review comments, tracked changes, deleted text, and metadata before sharing outputs.

Risk: Careless DOCX edits can cause layout drift, broken numbering, stale fields, or damaged review anchors across Word, LibreOffice, Google Docs, and conversion tools.

Mitigation: Favor minimal structure-preserving edits and verify round-trip compatibility in the target editor before delivery when layout or review fidelity matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonydesign1999/skills/word-docx-1)
- [Skill homepage](https://clawic.com/skills/word-docx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the skill artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
