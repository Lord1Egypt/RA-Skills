## Description:

OCR and text extraction from Word documents (.docx, .doc) using the MinerU API and mineru-open-api CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to run OCR on scanned or image-based Word documents, including contracts, reports, and legacy .doc files, with quick or advanced MinerU extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or regulated Word documents may be sent through a third-party OCR CLI.

Mitigation: Review MinerU data handling before use; prefer an isolated environment and avoid remote OCR for confidential, regulated, client, legal, or financial documents unless approved.

Risk: The skill recommends a global unpinned npm install for mineru-open-api.

Mitigation: Avoid administrator/root installs where possible, pin and verify the CLI package, and review token and billing terms before precision extraction.

## Reference(s):

- [MinerU API Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and output file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OCR output files under a generated MinerU-Skill output directory.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
