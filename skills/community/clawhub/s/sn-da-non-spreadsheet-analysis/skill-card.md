## Description:

Analyzes Word, PDF, and PowerPoint documents by extracting text, tables, numeric data, formatting, charts, and image-only content for cross-document analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to extract, verify, and analyze content from Word, PDF, and PowerPoint files. It supports multi-document summaries, table and numeric extraction, format checks, and chart or image-only page interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive document content may be written to predictable shared temporary paths during conversion, rendering, extraction, or captioning.

Mitigation: Install only in trusted single-user or well-sandboxed environments, use private per-run temporary directories, and delete rendered or extracted artifacts after use.

Risk: Scanned pages, image-only slides, embedded images, and charts may require image captioning that handles document-derived content.

Mitigation: Make captioning explicit and user-controllable, and avoid highly confidential contracts, invoices, resumes, or presentations unless the handling path is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-da-non-spreadsheet-analysis)
- [ClawHub publisher profile](https://clawhub.ai/user/sensenova-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with extracted text, tables, calculations, verification notes, and optional code or shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use format-specific document parsers and image captioning for scanned pages, image-only slides, embedded images, and charts; calculation outputs should include units and intermediate values.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
