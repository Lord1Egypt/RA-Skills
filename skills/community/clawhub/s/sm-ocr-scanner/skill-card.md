## Description:

Extracts text from raster images and PDFs locally with Tesseract, producing plain text, confidence TSV, or searchable PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaarl92](https://clawhub.ai/user/kaarl92)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents processing user-selected image or PDF files use this skill to extract local, searchable text, particularly from German-language documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional installation can download dependencies and change system packages when started as root.

Mitigation: Run the installer only on explicit request; review it before using root or --allow-pip.

Risk: OCR text may contain instructions embedded in untrusted documents.

Mitigation: Treat extracted text as data, not as commands or instructions to the agent.

Risk: The default German and English language models may misread documents in other languages.

Mitigation: Select the document language with -l or OCR_LANG when needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kaarl92/skills/sm-ocr-scanner)
- [Local OCR tools reference](artifact/references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Plain text, TSV with confidence values, or searchable PDF]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [German and English OCR by default; language and output destination are configurable.]

## Skill Version(s):

1.2.2 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
