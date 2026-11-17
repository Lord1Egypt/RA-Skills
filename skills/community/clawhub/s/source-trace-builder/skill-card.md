## Description:

Builds source indexes and original-source mappings for analytical drafts while distinguishing primary and secondary sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research workflow users use this skill to turn draft citations, source clues, and notes into a reviewable source directory with primary-versus-secondary distinctions, citation mappings, missing-source notes, risk notes, and maintenance suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script includes local audit and pattern-scanning modes beyond the advertised citation-tracing purpose.

Mitigation: Review the selected mode and intended input before execution, use deliberate output paths, and run only on files or directories that should be inspected.

Risk: The skill organizes local input and does not verify source facts online.

Mitigation: Treat missing or unverifiable citations as review items and confirm important claims against primary sources before publication or formal use.

Risk: Citation drafts may include sensitive or personal material from the user's input.

Mitigation: Remove or redact sensitive material before processing and avoid running directory scans on broader folders than necessary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/source-trace-builder)
- [README.md](artifact/README.md)
- [resources/spec.json](artifact/resources/spec.json)
- [resources/template.md](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report or JSON payload from the local helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a report to an explicit output path; supports dry-run and local input only.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
