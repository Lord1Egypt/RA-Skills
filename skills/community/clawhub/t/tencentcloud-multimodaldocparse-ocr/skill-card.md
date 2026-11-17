## Description:

Tencentcloud MultimodalDocParse OCR helps agents send document URLs to Tencent Cloud's MultimodalDocParse OCR API and return structured extraction results for PDF, Office, text, image, and WPS files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to extract content from user-provided document URLs into structured JSON, Markdown, XML, or downloaded ZIP results. It is suited for document parsing workflows involving contracts, invoices, reports, papers, resumes, tables, scanned images, and embedded document images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user document URLs and document contents to Tencent Cloud OCR.

Mitigation: Confirm user consent before processing confidential contracts, invoices, resumes, internal reports, or other sensitive documents.

Risk: Document URLs and downloaded result packages may expose sensitive content beyond the current session.

Mitigation: Prefer short-lived private URLs, write results to a private output directory, and delete downloaded ZIP files when they are no longer needed.

Risk: Tencent Cloud credentials are required for API access.

Mitigation: Use narrowly scoped credentials and avoid placing secrets directly in command history or shared files.

## Reference(s):

- [Tencent Cloud MultimodalDocParse API Documentation](https://cloud.tencent.com/document/product/866/133224)
- [Result Package Structure](references/result-package-structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The called API returns a temporary ZIP result URL; when download is enabled, the script writes the ZIP package to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
