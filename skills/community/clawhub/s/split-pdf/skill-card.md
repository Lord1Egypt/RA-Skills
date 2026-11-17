## Description:

Split a single PDF into multiple parts. Supports page ranges, per-page splitting, and fixed chunk splitting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to split PDFs into selected page ranges, individual pages, or a fixed number of chunks for extraction, sharing, storage, printing, or batch document processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF files or public PDF URLs are sent to pdfapihub.com for processing.

Mitigation: Do not submit confidential, regulated, internal-only, or third-party documents unless the provider's privacy, retention, and access controls have been reviewed and accepted.

Risk: Generated outputs may be hosted on the provider's CDN.

Mitigation: Use the skill only when CDN-hosted outputs are acceptable for the document sensitivity and access-control requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/skills/split-pdf)
- [PDF API Hub Documentation](https://pdfapihub.com/docs)
- [PDF API Hub Split Endpoint](https://pdfapihub.com/api/v1/pdf/split)

## Skill Output:

**Output Type(s):** [API Calls, Files, Shell commands, Configuration instructions]

**Output Format:** [JSON API request and response with PDF output as URLs, files, or base64, plus optional curl examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLIENT-API-KEY authentication; accepts a public PDF URL, base64-encoded PDF, or multipart file upload; source limits state max 200 pages per document and max 100 output chunks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
