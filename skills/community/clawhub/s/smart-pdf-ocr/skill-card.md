## Description:

Intelligent PDF OCR powered by MinerU API for extracting text from scanned PDFs, image-based PDFs, and photographed documents using the mineru-open-api CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to run OCR on scanned or image-based PDFs, including multilingual documents, complex layouts, tables, and formulas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external MinerU CLI/API and a global npm install.

Mitigation: Confirm trust in the mineru-open-api npm package and review the provider's privacy and retention terms before installation or use.

Risk: PDFs may contain sensitive contracts, receipts, regulated records, or private documents.

Mitigation: Avoid processing sensitive documents unless the MinerU provider's privacy, storage, and retention terms meet the user's requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and OCR output file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses mineru-open-api to create OCR extraction outputs in a local output directory.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
