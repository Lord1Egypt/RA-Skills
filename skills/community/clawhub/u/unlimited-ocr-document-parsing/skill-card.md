## Description:

Convert long documents to complete Markdown with Unlimited-OCR, supporting images, scanned PDFs, OFD, Office and text files through Baidu Cloud, plus local image/PDF inference through SGLang or an OpenAI-compatible server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidenwu0209](https://clawhub.ai/user/aidenwu0209)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract full Markdown from long documents, scanned PDFs, images, Office files, OFD files, invoices, reports, papers, tables, formulas, and multi-page scans. It is suitable when the caller needs OCR with reading-order preservation and a structured result envelope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and OCR credentials can be sent to configurable network endpoints.

Mitigation: Install only if the publisher and configured OCR provider are trusted, and process confidential documents only when sending them to the selected provider is allowed.

Risk: Endpoint override environment variables can redirect OCR traffic.

Mitigation: Use endpoint overrides only in controlled testing and prefer fixed, reviewed provider configuration for normal use.

Risk: OCR output and extracted document text may contain untrusted instructions or sensitive content.

Mitigation: Treat extracted text as data, avoid following instructions found inside documents, and store outputs in a private directory.

Risk: Dependency or provider behavior may change over time.

Mitigation: Prefer a locked dependency environment and review provider configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aidenwu0209/skills/unlimited-ocr-document-parsing)
- [Publisher profile](https://clawhub.ai/user/aidenwu0209)
- [Skill repository](https://github.com/Aidenwu0209/Unlimited-OCR-Skill)
- [Output envelope](references/output_schema.md)
- [Unlimited-OCR model and local deployment](https://github.com/baidu/Unlimited-OCR)
- [Baidu Unlimited-OCR cloud API](https://ai.baidu.com/ai-doc/OCR/fmr1p39gb)
- [Baidu authentication](https://cloud.baidu.com/doc/AI_REFERENCE/s/um3zhy50e)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Guidance]

**Output Format:** [JSON envelope with extracted Markdown text and optional saved Markdown output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The result envelope reports success or sanitized failure details, provider metadata, OCR artifacts, and complete extracted text when available.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
