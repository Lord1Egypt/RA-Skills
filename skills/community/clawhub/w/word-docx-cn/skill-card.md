## Description:

Helps agents create, inspect, and edit Microsoft Word DOCX documents while preserving styles, numbering, tracked changes, tables, sections, and compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document automation agents, and business users use this skill when working with Word or DOCX files that need careful handling of review metadata, formatting, numbering, page layout, tables, fields, and round-trip compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Word review files can contain sensitive comments, tracked changes, deleted text, and other review metadata.

Mitigation: Inspect and preserve review metadata deliberately, and remove or disclose it only when the user explicitly requests that outcome.

Risk: DOCX documents can appear correct while fields, references, numbering, tables, headers, or pagination drift after opening in another editor.

Mitigation: Use structure-aware DOCX handling and verify round-trip behavior in the target editor when layout or references matter.

Risk: Legacy or macro-bearing Word formats such as .doc and .docm can carry compatibility or execution risks.

Mitigation: Convert legacy .doc inputs before relying on DOCX assumptions and treat macro-bearing .docm files as higher risk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linbo405/skills/word-docx-cn)
- [Publisher profile](https://clawhub.ai/user/linbo405)
- [Original skill homepage](https://clawic.com/skills/word-docx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text guidance, with code or shell commands when document tooling is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation or editing of DOCX files while preserving document structure and review metadata.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
