## Description:

scnet-ocr lets an agent send a user-specified image or PDF to the SCNET OCR API and return extracted text, document fields, tables, seals, invoices, credentials, and financial-document data as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill when they need OCR for a specific local image or PDF, including general text, forms, identity documents, invoices, permits, medical bills, and financial documents. It is appropriate when the user has explicitly requested recognition and is authorized to upload the selected file to SCNET.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images or PDFs may contain sensitive personal, medical, identity, invoice, or financial information that is uploaded to SCNET for OCR.

Mitigation: Use only files the user is authorized to process, confirm before sensitive-document OCR, and upload only the minimum file needed for the task.

Risk: A changed SCNET_API_BASE value could redirect both the selected file and bearer token away from the intended SCNET endpoint.

Mitigation: Leave SCNET_API_BASE unset for the default endpoint or verify it is exactly the intended HTTPS SCNET API base before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/scnet-ocr)
- [SCNET service site](https://www.scnet.cn)
- [SCNET OCR API summary](references/api-docs.md)
- [SCNET OCR API endpoint](https://api.scnet.cn/api/llm/v1/ocr/recognize)

## Skill Output:

**Output Type(s):** [JSON, text, guidance]

**Output Format:** [JSON array printed to standard output, with privacy warnings and error messages emitted as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY; SCNET_API_BASE is optional and defaults to the SCNET HTTPS API base.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
