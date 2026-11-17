## Description:

Parses Chinese traffic accident legal documents, extracts legal article references, and generates markdown templates for traffic safety exam answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghaibo7612](https://clawhub.ai/user/zhanghaibo7612)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and legal operations users can use this skill to parse local Chinese traffic-law Word documents into structured JSON, look up article references, and produce review-ready traffic safety exam answer drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy local document text into JSON, Markdown, or text outputs, and generated answer files are templates rather than finished legal or exam answers.

Mitigation: Review input and output paths before running scripts, and have a qualified human review extracted legal text and generated answer drafts before relying on them.

Risk: Document parsing has format and environment limits, including simplified .docx parsing, manual handling for old .doc files, and a documented Microsoft Word dependency.

Mitigation: Confirm the local document format and runtime environment before batch processing, and inspect parser status fields for skipped or failed files.

## Reference(s):

- [Traffic accident legal articles quick reference](artifact/references/legal_articles.md)
- [ClawHub skill page](https://clawhub.ai/zhanghaibo7612/skills/traffic-law-doc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON for parsed law documents and Markdown or text files for exam-answer templates and extracted content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include copied source document text and should be reviewed before legal or exam use.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
