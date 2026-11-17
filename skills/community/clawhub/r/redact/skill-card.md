## Description:

Privacy redaction toolkit for images, PDFs, Word documents, and PowerPoint presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darknoah](https://clawhub.ai/user/darknoah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, privacy/compliance reviewers, and document handlers use this skill to read and redact sensitive text in images, PDFs, Word documents, and PowerPoint presentations before sharing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unredacted sensitive text may be left in temporary files or logs.

Mitigation: Run the skill in an isolated workspace, clean temporary directories after use, and avoid highly sensitive documents until cleanup and logging behavior are fixed.

Risk: Redaction can fail silently for embedded images in PowerPoint while still producing a saved output file.

Mitigation: Inspect generated presentations before sharing them and treat warnings during processing as blockers for release of the redacted file.

Risk: OCR-based redaction may miss text or preserve private content in unsupported document structures.

Mitigation: Review outputs manually before distribution and keep the original files separate from redacted deliverables.

## Reference(s):

- [Redact ClawHub skill page](https://clawhub.ai/darknoah/skills/redact)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts output extracted text, structured JSON, or redacted image/document/presentation files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the input file type and CSV redaction rules.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence; artifact pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
