## Description:

Calls Tencent Cloud OCR ExtractDocAgent to extract structured fields from images or PDFs using user-defined field names, field types, and prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to extract structured key-value and table fields from contracts, invoices, reports, and similar document images or single-page PDFs through Tencent Cloud OCR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document images, PDFs, or document URLs are sent to Tencent Cloud OCR for processing.

Mitigation: Use the skill only for documents approved for Tencent Cloud processing, and avoid highly sensitive contracts or invoices without organizational approval.

Risk: Tencent Cloud API credentials are required in the runtime environment.

Mitigation: Use narrowly scoped credentials and run the skill in an isolated environment with appropriate secret handling.

Risk: The Tencent Cloud SDK dependency may change behavior across versions.

Mitigation: Prefer a pinned SDK version when installing dependencies for repeatable operation.

## Reference(s):

- [Tencent Cloud ExtractDocAgent API Documentation](https://cloud.tencent.com/document/api/866/126442)
- [ClawHub Skill Page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-extractdocagent)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON response from a command-line Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formatted extraction output by default, with an option to return the raw Tencent Cloud OCR API response.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
