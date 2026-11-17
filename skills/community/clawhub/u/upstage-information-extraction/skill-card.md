## Description:

Extracts named fields from documents with the Upstage Information Extraction API using custom JSON schemas or prebuilt receipt, invoice, waybill, bill-of-lading, and export-certificate models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to guide agents in extracting specific named values from receipts, invoices, waybills, bills of lading, export certificates, and similar documents. It is intended for structured field extraction with a schema or supported prebuilt model, not general OCR or full document conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents sent for extraction may contain sensitive information and are uploaded to Upstage for processing.

Mitigation: Use the skill only when the user is comfortable sending the relevant documents to Upstage, and avoid submitting unnecessary pages or files.

Risk: Extracted JSON can contain sensitive business, financial, or personal data.

Mitigation: Prefer an explicit private output path with restricted permissions, avoid shared temporary directories, and delete saved JSON files when they are no longer needed.

## Reference(s):

- [Upstage Information Extraction API](https://console.upstage.ai/api/information-extraction)
- [ClawHub Skill Page](https://clawhub.ai/upstage-deployment/skills/upstage-information-extraction)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python examples, API request patterns, and JSON output file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent is instructed to save extracted data as JSON and report the resolved absolute output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
