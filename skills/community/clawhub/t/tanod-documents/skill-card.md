## Description:

Document conversion over HTTPS with Tanod: PDF, Word, Excel, PowerPoint, HTML or EPUB to Markdown; PDF tables to JSON, CSV or XLSX; OCR for images and scanned PDFs; PDF to Word; bank statement PDF to transactions. Pay per call with a small free daily allowance; every payment needs the user's approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanod-labs](https://clawhub.ai/user/tanod-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can convert common office documents, PDFs, images, and scanned files into Markdown, extracted text, structured tables, or other document formats. They can also extract bank statement transactions for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential documents and bank statements are uploaded to the hosted service, which was not audited; paid calls can incur charges.

Mitigation: Review the provider's data-handling and retention practices before uploading confidential files, and approve each private-document upload and every charge.

## Reference(s):

- [Tanod Documents on ClawHub](https://clawhub.ai/tanod-labs/skills/tanod-documents)
- [Tanod](https://tanod.dev)
- [Tanod OpenAPI specification](https://tanod.dev/openapi.json)
- [Tanod MCP endpoint](https://tanod.dev/mcp)

## Skill Output:

**Output Type(s):** [Plain text, Markdown, JSON, CSV, XLSX, DOCX, Searchable PDF, OFX, QIF]

**Output Format:** [Plain text or a document/table file, depending on the conversion route]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output format depends on the route; results may be inline or returned as a time-limited download URL.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
