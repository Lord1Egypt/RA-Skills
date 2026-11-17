## Description:

Diagnose and repair Microsoft Word DOCX formatting problems, including styles, numbering, section breaks, headers and footers, comments, tracked changes, and OOXML compatibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge workers, legal and operations teams, documentation maintainers, and developers use this skill to diagnose Word DOCX formatting failures and plan or implement careful repairs to styles, numbering, sections, headers, footers, comments, tracked changes, and OOXML compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect or modify sensitive DOCX files, including legal or business documents.

Mitigation: Keep an original backup, work on a copy, explicitly invoke the skill for confidential files, and review any repaired document before use.

Risk: Broad or unsupported OOXML edits can damage document structure, numbering, comments, or tracked changes.

Mitigation: Apply the smallest safe change, preserve comments and tracked changes unless cleanup is requested, and validate by reopening or rendering the document when possible.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/word-docx-formatting-repair-helper)
- [Publisher Profile](https://clawhub.ai/user/kyro-ma)
- [Markdown and Pandoc DOCX/PDF Demand Signal](https://segmentfault.com/a/1190000004887280)
- [Word Control Read-Only Demand Signal](https://segmentfault.com/a/1190000023469253)
- [Python Word Table Demand Signal](https://segmentfault.com/a/1190000044727832)
- [Word Line-Break Demand Signal](https://segmentfault.com/a/1190000040583144)
- [PDF/HTML to DOCX Demand Signal](https://segmentfault.com/a/1190000047409513)
- [.NET Track Changes Demand Signal](https://segmentfault.com/q/1010000005983758/a-1020000005984066)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional code, shell commands, configuration notes, and document repair plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation notes and remaining risks for repaired DOCX files]

## Skill Version(s):

1.0.1 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
